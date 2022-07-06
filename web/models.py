from ast import arg
from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from private_storage.fields import PrivateFileField
from smsServices.tasks import send_sms
from uuid import uuid4
from datetime import datetime


    


class Tag(models.Model):
    name  = models.CharField(max_length=225)
    color = ColorField(format="hexa", default="#00000")

    def __str__(self):
        return self.name



class ProfileStud(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_stud')
    major       = models.CharField(max_length=225, blank = True)
    is_verified = models.BooleanField(default=False)
    __original_is_verified = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_is_verified = self.is_verified

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.is_verified == True and self.__original_is_verified == False:
            send_sms.delay(self.user.phone, "Your account has been verified")
        super().save(*args, **kwargs)
        self.__original_is_verified = self.is_verified

    def __str__(self):
        return str(self.user.phone)

class ProfileMentor(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_mentor')
    is_verified = models.BooleanField(default=False)
    __original_is_verified = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_is_verified = self.is_verified

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.is_verified == True and self.__original_is_verified == False:
            send_sms.delay(self.user.phone, "Your account has been verified")
        super().save(*args, **kwargs)
        self.__original_is_verified = self.is_verified

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
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_projects')
    admissionNo  = models.PositiveIntegerField(default=1)
    is_active    = models.BooleanField(default=False)
    __original_is_active = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_is_active = self.is_active


    def save(self,force_insert=False, force_update=False, *args, **kwargs ):
        if self.is_active == True and self.__original_is_active == False:
            send_sms.delay(self.user.phone, f"Your project ({self.title}) has been approved")
        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_is_active = self.is_active
    


class RequestedProjects(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requested_projects')
    def __str__(self) -> str:
        return self.user.phone
    class  Meta:
        verbose_name = 'grouped requests by user request'
        verbose_name_plural = 'grouped requests by user request'

class RequestItem(models.Model):
    PENDING  = 'p'
    APPROVE  = 'A'
    REJECT   = 'R'
    STATUS =(
        (PENDING, 'Pending'),
        (APPROVE, 'Approve'),
        (REJECT,  'Reject'),
    )
    parent       = models.ForeignKey(RequestedProjects, on_delete=models.PROTECT, related_name='items')
    # TODO on delete project send email or sms to user
    project       = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='requests')
    status        = models.CharField(max_length=5, choices=STATUS, default=PENDING)
    passed        = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    passed_time   = models.DateTimeField(null=True, blank=True)
    approved_time = models.DateTimeField(null=True, blank=True)
    __original_status = None
    __original_passed = None

    class Meta:
        unique_together = ('parent', 'project')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status
        self.__original_passed = self.passed
    
    def save(self, *args, **kwargs):
        if self.status == self.APPROVE:
            stat = 'accepted by mentor'
        elif self.status == self.REJECT:
            stat = 'rejected by mentor'
        elif self.status == self.PENDING:
            stat = 'pending for mentor review'
        
        if self.status != self.__original_status and self.status != self.PENDING:
            send_sms.delay(self.parent.user.phone, "Your request for project {} is in status : {}, check your mentors message.".format(self.project.title, stat))
            if self.status == self.APPROVE:
                self.approved_time = datetime.now()
        if self.passed == True and self.__original_passed ==False:
            send_sms.delay(self.parent.user.phone, "congradulations you finished {} project .".format(self.project.title))
            self.passed_time = datetime.now()

        
        super().save(*args, **kwargs)
        self.__original_status = self.status
        self.__original_passed = self.passed

class MentorMessageForAdmission(models.Model):
    parent     = models.ForeignKey(RequestItem, on_delete=models.CASCADE, related_name='messages')
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        title = 'Mentor Message for Admission from user : '+ str(self.parent.project.user.phone) + ' to -> ' + str(self.parent.parent.user.phone) + ' .'
        return title







# class ApprovedRequest(models.Model):
#     user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='approved_projects_cart')

# class ApprovedItem(models.Model):
#     APPROVE   = 'A'
#     REJECT = 'R'
#     PASSED   = 'P'
#     APPROVED_STATUS = (
#         (APPROVE, 'Active'),
#         (REJECT, 'REJECTED'),
    #     (PASSED, 'Passed'),
    # )
    # parent              = models.ForeignKey(ApprovedRequest, on_delete=models.PROTECT, related_name='items', verbose_name='user_cart')
    # project             = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='approved_projects')
    # created_at          = models.DateTimeField(auto_now_add=True)
    # status              = models.CharField(choices=APPROVED_STATUS, default=APPROVE, max_length=5)
    # def __str__(self):
    #     return (str(self.parent.user.phone) + str(self.project.title))
    # class Meta:
    #     unique_together = ('parent', 'project')

