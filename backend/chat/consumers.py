# chat/consumers.py
import json
from urllib.parse import parse_qs
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from accounts.views import checkToken
from django.http import JsonResponse
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        query_string = self.scope.get('query_string').decode()
        query_params = parse_qs(query_string)
        self.jwt = query_params.get('token', [None])[0]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        ## we will allow user to connect from and send error message to socket and disconnect it
        self.authorizeChatRoom()


    def disconnect(self,close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"][0]
        self.jwt = event['message'][1]
        if  self.authorizeChatRoom():
            self.send(text_data=json.dumps({"message": message}))

    def authorizeChatRoom(self) ->bool:
        response = checkToken(jwtToken = self.jwt)
        if response['error']:
            self.send(text_data=json.dumps(response))
            self.disconnect()

            return False
        return True