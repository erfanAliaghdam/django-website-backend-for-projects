from rest_framework.response import Response
from .serializers import MessageSerializer, CreateTokenSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import Message, User
from ..permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import ValidationError
from smsServices.tasks import send_sms
from datetime import datetime
from django.utils import timezone

# Create your views here.

class MessageViewSet(ModelViewSet):
    serializer_class   = MessageSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated] 
    
    def get_queryset(self):
        return Message.objects.filter(reciever=self.request.user).all()


class CreateTokenViewSet(ModelViewSet):
    serializer_class   = CreateTokenSerializer
    http_method_names  = ['post']
    queryset           = User.objects.none()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']        
        try:
            user = User.objects.get(phone=phone)
            if (not user.otp_activated) and user.otpExpire < timezone.now():
                print('!-----<***||-o-||***>----!')
                print(send_sms.delay(phone))
                print('!-----<***||-o-||***>----!')
                # print(vars(user))
                # TODO will check otp verification time and send otp again if time is expired
                raise ValidationError('User already is not verified')
            refresh = RefreshToken.for_user(user)

            response =  {
                            'refresh': str(refresh),
                            'access' : str(refresh.access_token),
                        }
            return Response(response)
            
        except User.DoesNotExist:
            raise ValidationError("User does not exist")
