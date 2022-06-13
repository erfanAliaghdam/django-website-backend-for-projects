from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from django.utils.html import format_html
from uuid import uuid4




class Tag(models.Model):
    name  = models.CharField(max_length=225)
    color = ColorField(format="hexa", default="#00000")

    def __str__(self):
        return self.name

class ProfileStud(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    major = models.CharField(max_length=225)
    is_verified = models.BooleanField(default=False)


class ProfileMentor(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
class VerificationDoc(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    document = models.FileField(upload_to='web/uploads')

class Project(models.Model):
    title       = models.CharField(max_length=250)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    tag         = models.ManyToManyField(Tag, related_name='projects')

class RequestedProjects(models.Model):
    id   = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class RequestItem(models.Model):
    parent  = models.ForeignKey(RequestedProjects, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete = models.PROTECT)