from dataclasses import fields
from pyexpat import model
from djoser.serializers import (UserSerializer as BaseUserSerializer,
                                 UserCreateSerializer as BaseUserCreateSerializer)
from rest_framework import serializers
from ..models import Message, User

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'phone', 'is_mentor']
        


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'phone', 'is_mentor', 'password']
    



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Message
        fields = ['id', 'reciever', 'message', 'send_time', 'message_type']
        related_fields = ['reciever']    




class CreateTokenSerializer(serializers.Serializer):
    phone = serializers.CharField()
    class Meta:
        model  = User
        fields = ['phone']


class SendOtpSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)
    class Meta:
        model  = User
        fields = ['otpCode', 'phone']


class SignUpOtpSerializer(serializers.Serializer):
    phone = serializers.CharField()
    class Meta:
        model  = User
        fields = ['otpCode', 'phone', 'password']

