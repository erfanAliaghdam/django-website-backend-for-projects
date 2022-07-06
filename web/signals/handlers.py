from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.db.models import Q
from web.models import RequestItem, RequestedProjects, ProfileMentor, ProfileStud, RequestItem
from smsServices.tasks import send_sms


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    print("----|||||*****---*(<->)*---****|||||----")
    if kwargs['created']:
        if kwargs['instance'].__dict__['is_mentor']:
            ProfileMentor.objects.create(user=kwargs['instance'])
            print("-----automatically: Mentor Profile-----")
        else:
            ProfileStud.objects.create(user=kwargs['instance'])
            print("-----automatically: Stud Profile-----")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_RequestedProjRelation_for_new_user(sender, **kwargs):
    if kwargs['created']:
        RequestedProjects.objects.create(user=kwargs['instance'])
        print("-----automatically: RequestedProjectCart-----")


@receiver(post_save, sender=RequestItem)
def send_sms_on_apply(sender, **kwargs):
    if kwargs['created']:
        print("-----SmsSignal-----")
        send_sms.delay(kwargs['instance'].parent.user.phone, "You applied for a project, please wait for the approval")
        send_sms.delay(kwargs['instance'].project.user.phone, "You have a new request")



# @receiver(pre_save, sender=ProfileMentor)
# def send_sms_if_verify_mentor(sender, instance, **kwargs):
#     if instance.is_verified and ProfileMentor.objects.filter(pk=instance.pk, is_verified=False).exists():
#         print("-----SmsSignal-----")
#         send_sms.delay(instance.user.phone, "Your account has been verified")


# @receiver(pre_save, sender=ProfileStud)
# def send_sms_if_verify_mentor(sender, instance, **kwargs):
#     if instance.is_verified and ProfileStud.objects.filter(pk=instance.pk, is_verified=False).exists():
#         print("-----SmsSignal-----")
#         send_sms.delay(instance.user.phone, "Your account has been verified")

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_approved_projects_for_new_user(sender, **kwargs):
#     if kwargs['created']:
#         ApprovedRequest.objects.create(user=kwargs['instance'])
#         print("-----automatically: ApprovedRequest-----")

