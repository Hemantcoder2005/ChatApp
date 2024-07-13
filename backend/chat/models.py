from django.db import models
from accounts import models as accountUser
# Create your models here.
class Chats(models.Model):
    sendBy = models.ForeignKey(accountUser.User,default=None,on_delete=models.CASCADE) #User who generated Mssg
    textMssg = models.TextField(max_length= 1000,default="") # What's the mssg
    timeStamp = models.DateTimeField(auto_now_add=True) # At what time and date mssg is send
    seen = models.BooleanField(default=False) # At what time person see the mssg
    seenAt = models.DateTimeField(null=True)
    def __str__(self) -> str:
        return f'{self.sendBy} at {self.timeStamp}'
    class Meta:
        ordering = ['-timeStamp']

class ChatRoom(models.Model):
    chatRoomName = models.CharField(max_length=1000,unique=True,default="")
    members = models.ManyToManyField(accountUser.User,default=None)
    chats = models.ManyToManyField(Chats,default=None)
    def __str__(self) -> str:
        return f'{self.chatRoomName}'


