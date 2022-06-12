from django.db import models
from django.conf import settings
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=225)

class ProfileStud(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    major = models.CharField(max_length=225)
    is_verified = models.BooleanField(default=False)

class ProfileMentor(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    tag         = models.ManyToManyField(Tag)
 
class VerificationDoc(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    document = models.FileField()

class Project(models.Model):
    title       = models.CharField(max_length=250)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)


