from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self._meta.get_field('username')
        username.verbose_name = "personal id"
    phone           = models.PositiveIntegerField(unique=True)
    is_mentor       = models.BooleanField(default=False)
    USERNAME_FIELD  = "username"
    REQUIRED_FIELDS = ["phone"]

 