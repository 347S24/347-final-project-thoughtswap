# ASYNC VERSION
import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('self.scope["user"]')
        print(self.scope["user"])
        self.code = self.scope["url_route"]["kwargs"]["code"]
        self.room_group_name = "chat_%s" % self.code

        # Join room group
        print("self.room_group_name, self.channel_name")
        print(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_to_db(self, message, prompt, facilitator_id, code, author, swap=False):
        # Save Prompt to the database
        if swap:
            thought = DistributedThought.objects.get(thought=prompt)
            thought.answer = message
            thought.save()
        else:
            if prompt:
                prompt = prompt.strip()
                facilitator = Facilitator.objects.get(pk=facilitator_id)
                discussion = Discussion.objects.get(code=code)
                prompt_obj = Prompt.objects.create(author=facilitator,
                                                   content=prompt, discussion=discussion)
                discussion.prompt_set.add(prompt_obj)
                print('saved prompt: ', prompt)

            if message:
                facilitator = Facilitator.objects.get(pk=facilitator_id)
                discussion = Discussion.objects.get(code=code)
                prompt_obj = discussion.prompt_set.last()
                # group = discussion.group

                # partipant = Participant.objects.get(
                #     username=author, group=group)

                partipant = Participant.objects.get(
                    username=author)
                message = message.strip()
                Thought.objects.create(
                    content=message, prompt=prompt_obj, author=partipant)
                print('saved message: ', message, "with prompt: ",
                      prompt_obj, "and author: ", partipant)

    @database_sync_to_async
    def delete_from_db(self, message):
        message = message.strip()
        print('message', message)
        thought = Thought.objects.get(content=message)
        thought.delete()

    # Receive message from WebSocket
    async def receive(self, text_data):
        print('recieve')
        text_data_json = json.loads(text_data)
        print('text', text_data)
        message = text_data_json["message"]
        prompt = text_data_json["prompt"]
        facilitator_id = text_data_json["facilitator_id"]
        code = text_data_json["code"]
        author = text_data_json["author"]
        save = text_data_json["save"]
        swap = text_data_json["swap"]

        if swap:
            if save:
                await self.save_to_db(message, prompt, facilitator_id, code, author, True)
            else:
                await self.thought_swap(code, prompt)
            if 'distribution' in self.__dict__:
                swap = await database_sync_to_async(self.distribution.to_dict)()
                await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message,
                                    "prompt": prompt, "facilitator_id": facilitator_id, "author": author, "code": code, 'swap': swap})
        else:
            if save:
                await self.save_to_db(message, prompt, facilitator_id, code, author)
            elif not save and not prompt:
                # TODO: Get accurate prompt/discussion to delete from (need to get username somehow)
                await self.delete_from_db(message)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message,
                                    "prompt": prompt, "facilitator_id": facilitator_id, "author": author, "code": code}
            )
    # Receive message from room group

    async def chat_message(self, event):
        message = event["message"]
        prompt = event["prompt"]
        facilitator_id = event["facilitator_id"]
        code = event["code"]
        author = event["author"]

        # Send message to WebSocket
        if 'distribution' in self.__dict__:
            swap = await database_sync_to_async(self.distribution.to_dict)()
            await self.send(text_data=json.dumps({"message": message, "prompt": prompt, "facilitator_id": facilitator_id, "code": code, "author": author, 'swap': swap}))
        else:
            await self.send(text_data=json.dumps({"message": message, "prompt": prompt, "facilitator_id": facilitator_id, "code": code, "author": author}))


    @database_sync_to_async
    def thought_swap(self, code, prompt):
        discussion = Discussion.objects.get(code=code)
        prompt = Prompt.objects.get(content=prompt)
        thoughts = list(prompt.thought_set.all())
        group = discussion.group
        participants = group.participant_set.all()
        thought_dict = {thought.author: thought for thought in thoughts}
        print('thoughts', thoughts, '\n\n\n\n\n\n\n\n\n\n')

        unanswered = [
            participant for participant in participants if participant not in thought_dict.keys()]
        answered = [
            participant for participant in participants if participant in thought_dict.keys()]

        print('unanswered', unanswered, '\n\n\n\n\n\n\n\n\n\n')
        print('answerd', answered, '\n\n\n\n\n\n\n\n\n\n')
        try:
            dist = Distribution.objects.get(prompt=prompt)
            self.distribution = dist
        except ObjectDoesNotExist:
            print('no exists')
            distribution = Distribution(prompt=prompt)
            distribution.save()

            swap_dict = {}

            for participant in unanswered:
                thought = random.choice(thoughts)
                distributedThought = DistributedThought(
                    author=participant, thought=thought, distribution=distribution, answer=None)
                swap_dict[participant] = thought.content
                distributedThought.save()

            for _ in range(len(thoughts)):
                thought = random.choice(thoughts)
                participant = random.choice(answered)
                # if the participant gets their own thought, reassign a thought
                while (thought_dict[participant] == thought):
                    thought = random.choice(thoughts)

                distributedThought = DistributedThought(
                    author=participant, thought=thought, distribution=distribution, answer=None)

                # remove the participant and thought so they are not reassigned
                answered.remove(participant)
                del thoughts[thoughts.index(thought)]
                swap_dict[participant] = thought.content

                # Save to DB
                distributedThought.save()
            print('pre distribution')
            for thought in thought_dict:
                print(thought, thought_dict[thought])
            print('post distribution')
            for thought in swap_dict:
                print(thought, swap_dict[thought])
            self.distribution = distribution
        except MultipleObjectsReturned:
            print("Multiple Distributions found for this prompt.")
        return None

    # async def receive_json(self, content, **kwargs):
    #     prompt_text = content.get('prompt')
    #     id = content.get('facilitator_id')
    #     code = content.get('code')
    #     if prompt_text:
    #         # Save the prompt to the database
    #         await self.save_prompt(prompt_text, id, code)

    # async def save_prompt(self, content, id, discussion_code):
    #     facilitator = Facilitator.objects.get(pk=id)
    #     discussion = Discussion.objects.get(code=discussion_code)
    #     Prompt.objects.create(author=facilitator, content=content, discussion=discussion)
# SYNC VERSION
# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))
