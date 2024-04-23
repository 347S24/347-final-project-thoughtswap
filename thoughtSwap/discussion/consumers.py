# ASYNC VERSION
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Discussion, Prompt, Facilitator

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

    # Receive message from WebSocket
    async def receive(self, text_data):
        print('recieve')
        text_data_json = json.loads(text_data)
        print('text', text_data)
        message = text_data_json["message"]
        prompt = text_data_json["prompt"]
        facilitator_id = text_data_json["facilitator_id"]
        code = text_data_json["code"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "prompt": prompt, "facilitator_id": facilitator_id, "code": code}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # print('event', event, '\n\n\n\n\n\n\n\n\n\n')
        prompt = event["prompt"]
        facilitator_id = event["facilitator_id"]
        code = event["code"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "prompt": prompt, "facilitator_id": facilitator_id, "code": code}))

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