from datetime import datetime
from itsdangerous import Serializer
from rest_framework.response import Response
from .serializers import MessageSerializer, CreateTokenSerializer, SendOtpSerializer, SignUpOtpSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import Message, User, BaseUserManager
from ..permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from smsServices.tasks import send_sms
from rest_framework.decorators import action
from rest_framework import status
from datetime import datetime

class MessageViewSet(ModelViewSet):
    serializer_class   = MessageSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated] 
    
    def get_queryset(self):
        return Message.objects.filter(reciever=self.request.user).all()


class CreateTokenViewSet(ModelViewSet):
    http_method_names  = ['get', 'post', 'put']
    queryset           = User.objects.none()
    serializer_class   = CreateTokenSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']        
        try:
            User.objects.filter(phone=phone).exists()
            print('!-----<***||-o-||***>----!')
            print(send_sms.delay(phone))
            print('!-----<***||-o-||***>----!')
                # TODO will check otp verification time and send otp again if time is expired
            return Response({ 'phone':phone , 'message':f"otp code sent !. please check your phone and enter the otp code in actions otp section."})
        except User.DoesNotExist:
            raise ValidationError("user doesnt exist , create account.", code=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'], url_name='otp-signup', serializer_class=SignUpOtpSerializer)
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        try:
            User.objects.get(phone=phone)
            raise ValidationError("user already exists , login.", code=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            user = User.objects.create(phone=phone)
            user.set_password(BaseUserManager().make_random_password())
            user.save()
            print('!-----<***||-o-||***>----!')
            print(send_sms.delay(phone))
            print('!-----<***||-o-||***>----!')
            return Response({ 'phone':phone , 'message':f"user created successfully."}, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['POST'], url_name='otp-send', serializer_class=SendOtpSerializer)
    def otp(self, request, *args, **kwargs):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        user = User.objects.get(phone=phone)
        print(max(user.otpExpire.timestamp(), datetime.now().timestamp()))
        if max(user.otpExpire.timestamp(), datetime.now().timestamp()) == datetime.now().timestamp():
            raise ValidationError("otp code expired")
        elif user.otpCode == serializer.validated_data['otp']:
            user.otp_activated = True
            user.save()
            refresh = RefreshToken.for_user(user)
            response =  {
                            'refresh': str(refresh),
                            'access' : str(refresh.access_token),
                        }
            return Response({ 'token':response ,'phone':phone , 'message':f"otp code verified !. you can now login."}, status=status.HTTP_200_OK)
        elif user.otpCode != serializer.validated_data['otp']:
            raise ValidationError("otp code is not valid", code=status.HTTP_400_BAD_REQUEST)
        return Response({'---!!!---'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)