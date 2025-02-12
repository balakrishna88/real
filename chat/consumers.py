# consumers.py
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from .models import Room, Message
from account.models import Account

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract room ID from URL route
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            # Parse incoming WebSocket data
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')
            sender_id = text_data_json.get('sender_id')
            file_data = text_data_json.get('file', None)  # Base64-encoded file data

            # Fetch room and sender objects asynchronously
            room = await sync_to_async(Room.objects.get)(id=self.room_id)
            sender = await sync_to_async(Account.objects.get)(id=sender_id)

            # Create message object asynchronously
            new_message = await sync_to_async(Message.objects.create)(
                room=room,
                sender=sender,
                content=message
            )

            # Handle file upload if present
            file_url = None
            if file_data:
                try:
                    format, imgstr = file_data.split(';base64,')  # Extract file format and data
                    ext = format.split('/')[-1]  # Get file extension
                    file_name = f'message_{new_message.id}.{ext}'
                    file_content = ContentFile(base64.b64decode(imgstr), name=file_name)

                    # Save the file to the `file` field and update the database
                    await sync_to_async(new_message.file.save)(file_name, file_content, save=True)
                    file_url = new_message.file.url  # Get file URL after saving
                except Exception as e:
                    print(f"Error processing file: {e}")

            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'timestamp': str(new_message.timestamp),
                    'file_url': file_url,  # Include file URL in broadcast
                }
            )
        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp'],
            'file_url': event.get('file_url', None),  # Include file URL in response
        }))







# consumers.py
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
from .models import Group, GroupMessage
from account.models import Account

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract group ID from URL route
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_group_name = f'group_chat_{self.group_id}'

        # Join group chat group
        await self.channel_layer.group_add(
            self.group_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group chat group
        await self.channel_layer.group_discard(
            self.group_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            # Parse incoming WebSocket data
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')
            sender_id = text_data_json.get('sender_id')
            file_data = text_data_json.get('file', None)  # Base64-encoded file data

            # Fetch group and sender objects asynchronously
            group = await sync_to_async(Group.objects.get)(id=self.group_id)
            sender = await sync_to_async(Account.objects.get)(id=sender_id)

            # Create group message object asynchronously
            new_message = await sync_to_async(GroupMessage.objects.create)(
                group=group,
                sender=sender,
                content=message
            )

            # Handle file upload if present
            file_url = None
            if file_data:
                try:
                    format, imgstr = file_data.split(';base64,')  # Extract file format and data
                    ext = format.split('/')[-1]  # Get file extension
                    file_name = f'group_message_{new_message.id}.{ext}'
                    file_content = ContentFile(base64.b64decode(imgstr), name=file_name)

                    # Save the file to the `file` field and update the database
                    await sync_to_async(new_message.file.save)(file_name, file_content, save=True)
                    file_url = new_message.file.url  # Get file URL after saving
                except Exception as e:
                    print(f"Error processing file: {e}")

            # Broadcast message to group chat group
            await self.channel_layer.group_send(
                self.group_group_name,
                {
                    'type': 'group_chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'timestamp': str(new_message.timestamp),
                    'file_url': file_url,  # Include file URL in broadcast
                }
            )
        except Exception as e:
            print(f"Error in receive: {e}")

    async def group_chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp'],
            'file_url': event.get('file_url', None),  # Include file URL in response
        }))
    
    