from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import UserManager
from django.forms import ValidationError


class BaseUserManager(UserManager): 
    #* delete first 0 if exists
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')

        extra_fields.setdefault('otp_activated', False)
        user  = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password=None, **extra_fields)


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def phone_validator(phone):
        phone = phone.lstrip('0')
        if len(phone) == 10 and phone[:1] == '9':
            return phone
        else:
            raise ValidationError("enter a valid phone number")

    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10,11}$")
    username         = models.CharField(max_length=20, unique=False)
    phone            = models.CharField(unique=True, validators=[phoneNumberRegex, phone_validator], max_length=11)
    is_mentor        = models.BooleanField(default=False)
    otpCode          = models.CharField(max_length=6, blank=True, null=True)
    otp_activated    = models.BooleanField(default=False)
    otpExpire        = models.DateTimeField(auto_now=True)
    USERNAME_FIELD   = "phone"
    REQUIRED_FIELDS  = []

    objects = BaseUserManager()


    def __str__(self) -> str:
        return (str(self.phone) + " : " + str(self.first_name))



class Message(models.Model):
    ALERT = 'A'
    WARNING = 'W'
    NOTIFY = 'N'
    MESSAGE_TYPE_CHOICES = (
        (ALERT, 'Alert'),
        (WARNING, 'Warning'),
        (NOTIFY, 'Notify'),
    )
    reciever     = models.ManyToManyField(User, related_name="reciever")
    message      = models.TextField()
    send_time    = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(choices=MESSAGE_TYPE_CHOICES, default=NOTIFY, max_length=5)
    

