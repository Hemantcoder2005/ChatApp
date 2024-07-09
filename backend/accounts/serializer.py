from .models import User #Importing User model
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserSerialzer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
    def create(self, validated_data):
        try:
            user = User.objects.create(
                email=BaseUserManager.normalize_email(validated_data['email']),
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                password = make_password(validated_data['password'])
            )
            return user
        except Exception as error:
            print(error)
            return error
class LoginSerialzer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



