from django.db.models.signals import post_save
from django.dispatch import receiver
from web.models import VerificationDoc
from core.models import User
from smsServices.tasks import send_sms

@receiver(post_save, sender=VerificationDoc)
def Verify_if_All_Docs_Are_Accepted(sender, **kwargs):
    print("***$$$$$$$$$$$$$$***")
    try: 
        user = User.objects.prefetch_related('VerDocs', 'profile_mentor').get(pk=kwargs['instance'].user.id)
        if not user.profile_mentor.is_verified:
            if user.VerDocs.filter(is_accepted=VerificationDoc.ACCEPTED).count() == user.VerDocs.count():
                user.profile_mentor.is_verified = True
                user.profile_mentor.save()
                print("-----automatically: VerificationDoc-----")

    except:
        user = User.objects.prefetch_related('VerDocs', 'profile_stud').get(pk=kwargs['instance'].user.id)
        if not user.profile_stud.is_verified:
            if user.VerDocs.filter(is_accepted=VerificationDoc.ACCEPTED).count() == user.VerDocs.count():
                user.profile_stud.is_verified = True
                user.profile_stud.save()
                print("-----automatically: VerificationDoc-----")       
