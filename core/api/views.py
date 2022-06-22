from django.shortcuts import render
from .serializers import MessageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import Message
from ..permissions import IsAdminOrReadOnly
# Create your views here.

class MessageViewSet(ModelViewSet):
    serializer_class   = MessageSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated] 
    
    def get_queryset(self):
        return Message.objects.filter(reciever=self.request.user).all()