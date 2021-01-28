from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from .models import *
import asyncio, json
from channels.layers import get_channel_layer
from django.db.models import Q
from datetime import datetime

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        if not self.scope["user"].is_authenticated:
            print("WARNING\tAttempted unauthenticated connection.")
            return

        self.user = self.scope["user"]
        self.account = Account.objects.get(user=self.user)
        self.room_hash = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.user.username
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

        chat_history = Message.objects.filter(
            Q(receiver=self.account) | Q(sender=self.account)
        ).order_by("timestamp")

        for message in chat_history:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": message.text,
                    "sender": message.sender.user.username,
                    "timestamp": str(message.timestamp).split(".")[0], 
                    "receiver": message.receiver.user.username,
                    "id": message.id,
                }
            )

    def receive(self, text_data=None, bytes_data=None):

        if not self.user.is_authenticated:
            print(f"{self.user} is not authenticated!")
            return 

        payload = json.loads(text_data)
        action = payload["action"]
        channel_layer = get_channel_layer()

        if action == "delete":
            print("DELETING!")
            msg_id = payload["id"]
            msg = Message.objects.get(id=msg_id)
            send_to = (msg.sender.user.username, msg.receiver.user.username)

            for channel in send_to:
                async_to_sync(channel_layer.group_send)(
                    channel,
                    {
                        "type": "delete.message",
                        "id": msg_id,
                    }
                )
            msg.delete()
            
        else:
            message = payload["message"]
            sender = self.account

            receiver_user = User.objects.get(username=payload["receiver"])
            receiver = Account.objects.get(user=receiver_user)

            msg_obj = Message(
                sender=sender,
                receiver=receiver,
                text=message
            )
            msg_obj.save()
    
            send_to = [receiver_user.username, self.user.username]

            for channel in send_to:
                async_to_sync(channel_layer.group_send)(
                    channel,
                    {
                        "type": "chat.message",
                        "message": message,
                        "sender": self.user.username,
                        "receiver": receiver_user.username,
                        "timestamp": str(datetime.now()).split(".")[0],
                        "id": msg_obj.id
                    }
                )

    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        receiver = event["receiver"]
        timestamp = event["timestamp"]
        msg_id = event["id"]

        self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "receiver": receiver,
            "timestamp": timestamp,
            "id": msg_id,
            "action": "receive"
        }))

    def delete_message(self, event):
        msg_id = event["id"]

        self.send(text_data=json.dumps({
            "id": msg_id,
            "action": "delete"
        }))

    
    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.account.name,
            self.room_hash
        )
        print("User disconnected!")


        
