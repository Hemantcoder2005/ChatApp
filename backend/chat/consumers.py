import json
from urllib.parse import parse_qs
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from accounts.views import checkToken
from .models import ChatRoom as ChatRoomDB
from .models import Chats as ChatsDB
from accounts.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        '''Helps to connect to websocket'''

        # roomName from url
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        # getting jwt key from url
        query_string = self.scope.get('query_string').decode()
        query_params = parse_qs(query_string)
        self.jwt = query_params.get('token', [None])[0]

        print(f"Connecting: JWT={self.jwt}, Room={self.room_name}")

        # Authorize user before allowing to connect
        autherizationResponse = self.authorizeChatRoom()
        if not autherizationResponse[0]:
            print("Authorization failed")
            self.close(4001) 
            return
        
        # Creating chatRoom in Database
        '''
            User1Id = 1
            User2Id = 2
            then ChatRoom in database is 1-2 to make it unique
        '''
        user1Id,user2Id = int(self.room_name),int(autherizationResponse[1])
        self.room_name = f'{min(user1Id,user2Id)}-{max(user1Id,user2Id)}'
        self.room_group_name = f"chat_{self.room_name}"
        self.users = [user1Id,user2Id]
        
        # Now running Basic test for db
        self.dbExist(self.room_name)
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        # Now we have load history to chats
        ####  self.loadHistory(full=True) --> Have to on this

        # setting recieved state False
        self.isReceived = False
        print(f"Connected: {self.channel_name}")

    def disconnect(self, close_code):
        '''This helps to disconnect user from websocket'''
        print(f"Disconnecting: {self.channel_name}, Close code: {close_code}")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        '''This help to user to receive mssg in a socket'''
        
        # Loading json data
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        # Setting received State to True otherwise it run saveMssg twice
        self.isReceived = True

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message,}
        )

    def chat_message(self, event):
        '''This will send message in a socket'''

        # Loading message from event (frontend)
        message = event["message"][0]
        
        # Handling error while sending mssg
        try:
            self.send(text_data=json.dumps({
                "user" : self.users[1],
                "message": message
                }))
            
            # Handling twice running when self.received runs it
            if not self.isReceived:
                self.saveMssg(message)
            else:
                self.isReceived = False
        except Exception as e:
            print(f"Error sending message: {e}")
            self.close(1000)
            print("Socket Closed!")

    def authorizeChatRoom(self):
        '''This will authorize chat by jwt key'''
        response = checkToken(jwtToken=self.jwt)
        if response.get('error'):
            print("Authorization error:", response['error'])
            return False,None
        return True,response['userId']
    
    def createUserInstance(self):
        '''This will create user Instance'''
        self.usersInstance = []
        for user in self.users:
            self.usersInstance.append(User.objects.get(id = user))

    def dbExist(self, chatRoom):
        '''This will help creating or loading database for a particular chatRoom'''
        print(self.users)
        self.createUserInstance()
        try:
            self.chatRoomDB = ChatRoomDB.objects.get(chatRoomName=chatRoom)
        except ChatRoomDB.DoesNotExist:
            # Creating chat room if it doesn't exist
            self.chatRoomDB = ChatRoomDB.objects.create(chatRoomName=chatRoom)
            print(self.usersInstance)
            self.chatRoomDB.members.add(*self.usersInstance)
        except Exception as e:
            print(f"Error accessing database: {e}")

    def saveMssg(self, mssg):
        '''This will save mssg after every chat'''
        try:
            if len(self.usersInstance) > 1:
                mssgInstance = ChatsDB.objects.create(sendBy=self.usersInstance[1], textMssg=mssg)
                self.chatRoomDB.chats.add(mssgInstance)
                print("Message saved successfully")
            else:
                print("Error: No valid user instance found")
        except Exception as e:
            print(f"Error saving message: {e}")

    def loadHistory(self,full=False):
        '''This will help in loading history while opening up chat'''
        history = self.chatRoomDB.chats.all()
        for mssg in history:
            self.send(text_data=json.dumps({
                "user" : self.users[1],
                "message": mssg
                }))