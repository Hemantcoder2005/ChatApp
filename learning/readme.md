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
