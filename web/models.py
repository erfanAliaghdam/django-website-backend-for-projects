from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from private_storage.fields import PrivateFileField
from uuid import uuid4




class Tag(models.Model):
    name  = models.CharField(max_length=225)
    color = ColorField(format="hexa", default="#00000")

    def __str__(self):
        return self.name

class ProfileStud(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_stud')
    major       = models.CharField(max_length=225, blank = True)
    is_verified = models.BooleanField(default=False)
    
class ProfileMentor(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_mentor')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.phone)


class VerificationDoc(models.Model):
    ACCEPTED ='A'
    REJECTED ='R'
    PENDING = 'P'
    ACCEPTANCE_STATUS = (
        (ACCEPTED  , 'Accepted'),
        (REJECTED  , 'Rejected'),
        (PENDING   , 'Pending'),
    )

    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='VerDocs')
    document            = PrivateFileField('File')
    created_at          = models.DateTimeField(auto_now_add=True)
    is_accepted         = models.CharField(choices=ACCEPTANCE_STATUS, max_length=10, default=PENDING)



class Project(models.Model):
    title        = models.CharField(max_length=250)
    slug         = models.SlugField(auto_created=True)
    description  = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)
    tag          = models.ManyToManyField(Tag, related_name='projects')
    is_active    = models.BooleanField(default=True)
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_projects')
    admissionNo  = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.title


class RequestedProjects(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requested_projects')

class RequestItem(models.Model):
    PENDING  = 'p'
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
    message_from_mentor = models.TextField(blank=True, null=True)

class ApprovedRequest(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='approved_projects_cart')

class ApprovedItem(models.Model):
    ACTIVE   = 'A'
    CANCELED = 'C'
    PASSED   = 'P'
    APPROVED_STATUS = (
        (ACTIVE, 'Active'),
        (CANCELED, 'Canceled'),
        (PASSED, 'Passed'),
    )
    parent              = models.ForeignKey(ApprovedRequest, on_delete=models.PROTECT, related_name='items', verbose_name='user_cart')
    project             = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='approved_projects')
    created_at          = models.DateTimeField(auto_now_add=True)
    status              = models.CharField(choices=APPROVED_STATUS, default=ACTIVE, max_length=5)
    message_from_mentor = models.TextField(blank=True)
    def __str__(self):
        return (str(self.parent.user.phone) + str(self.project.title))
    class Meta:
        unique_together = ('parent', 'project')

