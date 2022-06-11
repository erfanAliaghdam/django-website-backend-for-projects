from django.db import models
from django.contrib.auth.models import AbstractUser 
from . import apps
# Create your models here.



class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self._meta.get_field('username')
        username.verbose_name = "personal id"
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True)
    EMAIL_FIELD = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]
