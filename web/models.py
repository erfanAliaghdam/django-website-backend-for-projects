from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
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
    slug        = models.SlugField(auto_created=True)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    tag         = models.ManyToManyField(Tag, related_name='projects')
    is_active   = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class RequestedProjects(models.Model):
    id   = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requested_projects')

class RequestItem(models.Model):
    PENDING = 'p'
    APPROVED = 'A'
    REJECTED = 'R'
    STATUS =(
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    parent  = models.ForeignKey(RequestedProjects, on_delete=models.PROTECT, related_name='items')
    # TODO on delete project send email or sms to user
    project = models.ForeignKey(Project, null=True,on_delete=models.SET_NULL, related_name='requests')
    status  = models.CharField(max_length=5, choices=STATUS, default=PENDING)


class ApprovedRequest(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return (str(self.user.username) + str(self.project.title))

class ApprovedItem(models.Model):
    ACTIVE   = 'A'
    CANCELED = 'C'
    PASSED   = 'P'
    APPROVED_STATUS = (
        (ACTIVE, 'Active'),
        (CANCELED, 'Canceled'),
        (PASSED, 'Passed'),
    )
    parent     = models.ForeignKey(ApprovedRequest, on_delete=models.PROTECT)
    project    = models.ForeignKey(Project, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    status     = models.CharField(choices=APPROVED_STATUS, default=ACTIVE, max_length=5)

    def __str__(self):
        return (str(self.user.username) + str(self.project.title))
    