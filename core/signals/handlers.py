from django.db.models.signals import post_save
from django.dispatch import receiver
from web.models import VerificationDoc
from core.models import User

@receiver(post_save, sender=VerificationDoc)
def Verify_if_All_Docs_Are_Accepted(sender, **kwargs):
    print("***$$$$$$$$$$$$$$***")
    user = User.objects.prefetch_related('VerDocs', 'profile').get(pk=kwargs['instance'].user.id)
    if not user.profile.is_verified:
        if user.VerDocs.filter(is_accepted=VerificationDoc.ACCEPTED).count() == user.VerDocs.count():
            user.profile.is_verified = True
            user.profile.save()
            print("-----automatically: VerificationDoc-----")

    else:
        if user.VerDocs.filter(is_accepted=VerificationDoc.ACCEPTED).count() != user.VerDocs.count():
            user.profile.is_verified = False
            user.profile.save()
            print("-----automatically: VerificationDoc-----")
