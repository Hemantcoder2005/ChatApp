import json # For json response
from asgiref.sync import sync_to_async # This is for sync to database
from channels.generic.websocket import AsyncWebsocketConsumer # Websocket

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        '''This Function helps in connecting people in a group.'''
        self.roomName = self.scope['url_route']['kwargs']['room_name']
        self.roomGroupName = f'chat_{self.roomName}'
        # Join Room Name
        await self.channel_layer.group_add(self.roomGroupName,self.channel_name)
        await self.accept()
    async def disconnect(self, closeCode):
        '''This Function helps in disconnecting people from a group.'''
        # Leave Room
        await self.channel_layer.group_discard(self.roomGroupName,self.channel_name)


