import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from ..models import Notification

logger = logging.getLogger(__name__)


__all__ = ["send_mailings"]


@shared_task(ignore_result=True)
def send_mailings():
    logging.info("Start celery send_mailings task")
    notifications = Notification.objects.filter(is_done=False).filter(execute_at__lte=timezone.now())
    logging.info(f"Available notifications: {notifications}")
    for notification in notifications:
        recipients = set(notification.recipients.values_list("email", flat=True))
        recipients.add(notification.user.email)
        send_mail(
            "Admitad Notification",
            f"Title: {notification.title}\n"
            f"Description: {notification.description}\n"
            f"Location: {notification.location}"
            f"Event datetime: {notification.execute_at}",
            settings.EMAIL_HOST_USER,
            recipients,
            fail_silently=False,
        )
        notification.is_done = True
        notification.save()
    logging.info("End celery send_mailings task")
