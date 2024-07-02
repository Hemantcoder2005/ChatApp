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
- Add daphne to your settings.py INSTALLED_APPS
- Please ensure daphane is added front of dist

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
- Run it 3 or more to create users.
- Now run your server by
```bash
python manage.py runserver
```
- Now go to http://127.0.0.1:8000/admin
- login in django adminstration