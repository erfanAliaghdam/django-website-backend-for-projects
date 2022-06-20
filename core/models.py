from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self._meta.get_field('username')
        username.verbose_name = "personal id"
    phone           = models.PositiveBigIntegerField(unique=True)
    is_mentor       = models.BooleanField(default=False)
    USERNAME_FIELD  = "username"
    REQUIRED_FIELDS = ["phone"]

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
    