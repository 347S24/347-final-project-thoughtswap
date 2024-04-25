# ASYNC VERSION
import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async

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
    def save_to_db(self, message, prompt, facilitator_id, code, author):
        # Save Prompt to the database
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
            prompt_obj = discussion.prompt_set.all()[0]
            group = discussion.group

            partipant = Participant.objects.create(username=author, group=group)
            message = message.strip()
            Thought.objects.create(
                content=message, prompt=prompt_obj, author=partipant)
            print('saved message: ', message, "with prompt: ", prompt_obj, "and author: ", partipant)

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
        delete = text_data_json["delete"]

        if save:
            await self.save_to_db(message, prompt, facilitator_id, code, author)
        if delete:
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
        await self.send(text_data=json.dumps({"message": message, "prompt": prompt, "facilitator_id": facilitator_id, "code": code, "author": author}))

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
