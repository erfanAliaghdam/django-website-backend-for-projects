from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.db.models import Q
from web.models import RequestedProjects, ProfileMentor, ProfileStud




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    print("----|||||*****--\|-*(<->)*-|/--****|||||----")
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


