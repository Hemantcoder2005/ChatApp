import json
from urllib.parse import parse_qs
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from accounts.views import checkToken
from .models import ChatRoom as ChatRoomDB
from .models import Chats as ChatsDB
from accounts.models import User
from helper import *
class Consumer(WebsocketConsumer):
    '''There will be communication between Server and User only'''
    def connect(self):
        '''Helps to connect to websocket'''
        try:
            # roomName from url
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            # getting jwt key from url
            query_string = self.scope.get('query_string').decode()
            query_params = parse_qs(query_string)
            self.jwt = query_params.get('token', [None])[0]

            # Authorize user before allowing to connect
            autherizationResponse = self.authorizeChatRoom()
            if not autherizationResponse[0]:
                print_colored("Authorization failed","red")
                self.close(4001) 
                
            
            # Creating chatRoom in Database
            '''
                User1Id = 1
                User2Id = 2
                then ChatRoom in database is 1-2 to make it unique
            '''
            self.user = int(self.room_name)
            self.room_group_name = f"chat_{self.room_name}" 
            
            # Now running Basic test for db
            self.dbExist(self.room_name)
            
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()
            print_colored(f"UserConnected to Notification : {self.usersInstance} ","green")
            self.usersInstance.is_online = True
        except Exception as e:
            print(e)

    def disconnect(self, close_code):
        '''This helps to disconnect user from websocket'''
        print_colored(f"Disconnecting: {self.channel_name}, Close code: {close_code}","blue")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.usersInstance.is_online = False

    def receive(self, text_data):
        '''This help to user to receive mssg in a socket'''
        # Loading json data
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
       
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message,}
        )
        print_colored(f"{self.usersInstance[1]} = {message}","magenta")
        self.saveMssg(message)

    def chat_message(self, event):
        '''This will send message in a socket'''

        # Loading message from event (frontend)
        message = event["message"]
        
        # Handling error while sending mssg
        try:
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                "user" : self.users[1],
                "message": message
                }))
        except Exception as e:
            print_colored(f"Error sending message: {e}","red")
            self.close(1000)
            print_colored("Socket Closed!","blue")

    def authorizeChatRoom(self):
        '''This will authorize chat by jwt key'''
        response = checkToken(jwtToken=self.jwt)
        if response.get('error'):
            print_colored(f"Authorization error: {response['error']}","red")
            return False,None
        return True,response['userId']
    
    def createUserInstance(self):
        '''This will create user Instance'''
        self.usersInstance = User.objects.get(id = self.user)

    def dbExist(self, chatRoom):
        '''This will help creating or loading database for a particular chatRoom'''
        self.createUserInstance()
        try:
            self.chatRoomDB = ChatRoomDB.objects.get(chatRoomName=chatRoom)
            print_colored("DataBase exist!","green")
        except ChatRoomDB.DoesNotExist:
            # Creating chat room if it doesn't exist
            self.chatRoomDB = ChatRoomDB.objects.create(chatRoomName=chatRoom)
            print(self.usersInstance)
            self.chatRoomDB.members.add(*self.usersInstance)
            print_colored("dataBaseCreated","blue")
        except Exception as e:
            print_colored(f"Error accessing database: {e}","red")

    def saveMssg(self, mssg):
        '''This will save mssg after every chat'''
        try:
            if len(self.usersInstance) > 1:
                mssgInstance = ChatsDB.objects.create(sendBy=self.usersInstance[1], textMssg=mssg)
                self.chatRoomDB.chats.add(mssgInstance)
                print_colored("Message saved successfully","green")
            else:
                print_colored("Error: No valid user instance found","red")
        except Exception as e:
            print_colored(f"Error saving message: {e}","red")

    def loadHistory(self,full=False):
        '''This will help in loading history while opening up chat'''
        history = self.chatRoomDB.chats.all()
        chatHistory = []
        for mssg in history:
            chatHistory.append({
                'user' : "You" if mssg.sendBy.email == self.usersInstance[1].email else mssg.sendBy.email ,
                'content' : mssg.textMssg,
                'timeStamp': mssg.timeStamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        print_colored("ChatHistory Loaded Successfully","green")
        self.send(text_data=json.dumps({
            'type' : 'chat_history',
            'user':self.usersInstance[1].email,
            'history' :chatHistory
        }))

