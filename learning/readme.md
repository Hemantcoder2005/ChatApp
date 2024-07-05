# What is WebSockets?
WebSockets is a communication protocol that provides a consistent connection between a client and a server.

# HTTP synchronous vs WebSocket asynchronous
## HTTP synchronous
  <img src="srcs/1.png" alt="HTTP synchronous">

  ## WebSocket asynchronous
  <img src="srcs/2.png" alt="WebSocket asynchronous">   

## Understanding Implementation
<img src="srcs/3.png" >

### HTTP REQUEST.
- Browser send request to Server and Server send back handshake message
- In this phase we will use urls.py, views.py and return statement to return response.
### Upgradation to Webscokets
- Now, We will upgrade http request to django channel.
- In this phase, we will use routing.py, consumers.py and send() function.
### Upgradation to Channel Layer
- Now, We will upgrade Webscokets to Channel layer.
- This feature is useful when we have to send message in groups.
- In this phase, we will use async_to_sync,group_send() function.

# Let's Start!
## Create Virtul Environment
### Create
```bash
python -m venv env
```
### Activate
#### Linux or Mac
```bash
source env/bin/activate
```
#### Windows
```bash
env\Scripts\activate
```
## Installation
```bash
pip install -r requirements.txt
```
requirements.txt is  present in github repo.

## startproject
```bash
djangoadmin startproject learning
```
- You can also replace learning with your project name.
## Add daphne
- Go to settings.py add following codes
```python
INSTALLED_APPS = [
    'daphne',
    # Rest of all your apps.
]
```
Note in above code daphne should added at the top.
```python
CHANNELS_LAYERS = {
    'default':{
        'BACKEND' : 'channels.layers.InMemoryChannelLayer'
    }
}
```
```python
ASGI_APPLICATION = 'learning.asgi.application'
```
## Points to Be noted
- In this we will not discuss about authentication system.
- As we will create 3 superuser by running following commands
- First Make migrations
```bash
python manage.py migrate 
```
```bash
python manage.py createsuperuser
``` 
- Run it 3 or more times to create multiple users.
- Now run your server by
```bash
python manage.py runserver
```
- You can also see server running and also stated Starting ASGI/Daphne (This means we have successfully setup daphne😊)
- Now go to http://127.0.0.1:8000/admin
- login in django adminstration


## Creating Chat App
### Consumers and routing
- Starting a new app
```bash
python manage.py startapp chat
```
- register your app in INSTALLED_APPS
```python
INSTALLED_APPS = [
    # Rest of all your apps.
    'chat',
]
```
#### Consumer
- Create consumer.py under your chat app.
```python
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
```
#### Routing
- create routing.py under chat
```python
from django.urls import path
from . import consumers

websockets_urlspattern = [
    path('ws/<str:room_name',consumers.ChatConsumer.as_asgi())
]
```

### Updating asgi.py under settings.py
```python
import os

from django.core.asgi import get_asgi_application

# Imported 
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning.settings')

application = ProtocolTypeRouter(
    {
        'http' : get_asgi_application(),
        'websocket' : AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websockets_urlspattern))
        ) 
    }
)
```
#### Understanding above code
##### AuthMiddlewareStack
- The AuthMiddlewareStack provides authentication middleware for your Channels application. It wraps around your WebSocket consumer to handle user authentication, similar to how Django's authentication middleware works for HTTP views.
- It ensures that the user making a WebSocket connection is authenticated, allowing you to access the user through the connection scope (self.scope['user']).
##### AllowedHostsOriginValidator:
- The AllowedHostsOriginValidator middleware ensures that WebSocket connections come from allowed hosts, providing a security measure against Cross-Site WebSocket Hijacking (CSWSH).
- It checks the Origin header of incoming WebSocket requests to ensure that the request is coming from an allowed host as defined in your Django ALLOWED_HOSTS setting.
##### ProtocolTypeRouter
- The ProtocolTypeRouter is the main router in Channels that directs incoming connections to the appropriate application based on the protocol type (e.g., HTTP, WebSocket).
- It allows you to specify different routing mechanisms for different types of protocols (HTTP, WebSocket, etc.).
#### URLRouter
- The URLRouter routes WebSocket connections to the appropriate consumer based on the URL.
- It maps URL patterns to their corresponding consumers, similar to how Django's URL routing works for HTTP views.

### Modal For chat (database)
- Make changes to models.py under chat
```python
from django.db import models
from django.contrib.auth.models import User  # Importing user model from django default auth system

# Create your models here.
class Message(models.Model):
    body = models.TextField()
    sentBy = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    created_By = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('createdAt',)  
    def __str__(self) -> str:
        return f'{self.sentBy}'

class Room(models.Model):
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(User, related_name='rooms', blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('createdAt',)  
    def __str__(self) -> str:
        return f'{self.client}'
```
```bash 
python manage.py makemigrations
```
```bash 
python manage.py migrate
```
- Now, We have to register our model under Admin.py
```python
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Message)
admin.site.register(Room)
```
- Run server if it is running that's great!
- Now go to http://127.0.0.1:8000/admin

### Creating index.html to make browser and server interact

- in settings.py
```python
TEMPLATES = [
    {
        # your code
        'DIRS': [os.path.join(BASE_DIR,'templetes')],
        # your code
    },
]

```
#### ProTip
Want to use django like Live Server for avoiding reloading
```bash 
pip install django-browser-reload
```
```python
INSTALLED_APPS = [
    ...,
    "django_browser_reload",
    ...,
]
```
```python
MIDDLEWARE = [
    # ...
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    # ...
]
```
In urls.py

```python
from django.urls import include, path
urlpatterns = [
    ...,
    path("__reload__/", include("django_browser_reload.urls")),
]
```
- Create a file name templetes under your project
- Inside it create index.html
```html

```
