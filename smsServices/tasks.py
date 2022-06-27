from celery import shared_task
from django.utils.crypto import get_random_string
from django.conf import settings
from core.models import User
from datetime import timedelta
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_sms(phone):
    otp = get_random_string(length=6, allowed_chars='0123456789')
    logger.debug("Sending SMS to %s: %s" % (phone, str(otp)))
    user = User.objects.get(phone=phone)
    user.otpExpire = timezone.now() + timedelta(minutes = settings.EXPIRE_CODE_AFTER_MINUTES)
    user.otpCode   = str(otp)
    user.save()
    
    return str(otp)
