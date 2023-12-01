import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import ChatRoom, Message  # Assuming Message is defined in your models
from django.contrib.auth.models import User



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        
        # Save the message to the database
        await self.save_message(self.room_id, self.scope['user'].id, message_content)

        # Send to the sender with the fromSender flag set to True
        await self.send(text_data=json.dumps({
            'message': message_content,
            'fromSender': True
        }))

        # Broadcast to everyone else without the fromSender flag or with it set to False
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender_channel_name': self.channel_name  # Add this line to differentiate the sender
            }
        )


    async def chat_message(self, event):
        message = event['message']

        # Do not send the message back to the sender
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'message': message,
                'fromSender': False
            }))


    @database_sync_to_async
    def save_message(self, room_id, user_id, content):
        room = ChatRoom.objects.get(id=room_id)
        user = User.objects.get(id=user_id)
        Message.objects.create(room=room, sender=user, content=content)
