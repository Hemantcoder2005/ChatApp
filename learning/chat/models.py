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
