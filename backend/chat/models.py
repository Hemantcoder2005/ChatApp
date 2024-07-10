from django.db import models
from accounts import models as accountUser
# Create your models here.
class ChatRoom(models.Model):
    members = models.ManyToManyField(accountUser.User)