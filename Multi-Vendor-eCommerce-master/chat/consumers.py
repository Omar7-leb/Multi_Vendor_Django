# chat/consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from customers.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def create_chat(self, msg, sender, receiver, room_name):
        sender = User.objects.get(email = sender)
        receiver = User.objects.get(email = receiver)
        Message.objects.create(sender=sender, receiver=receiver, content=msg, room_name=room_name)

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        receiver = text_data_json["receiver"]
        room_name = text_data_json["room_name"]

        await self.create_chat(sender=sender, msg=message, receiver=receiver, room_name=room_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "sender": sender, "receiver":receiver}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
