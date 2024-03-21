import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from ..models import Reminder

logger = logging.getLogger(__name__)


__all__ = ["send_mailings"]


@shared_task(ignore_result=True)
def send_mailings():
    logging.info("Start celery send_mailings task")
    reminders = Reminder.objects.filter(is_done=False).filter(execute_at__lte=timezone.now())
    logging.info(f"Available reminders: {reminders}")
    for reminder in reminders:
        recipients = set(reminder.recipients.values_list("email", flat=True))
        recipients.add(reminder.user.email)
        send_mail(
            "Admitad Reminder",
            f"Title: {reminder.title}\n"
            f"Description: {reminder.description}\n"
            f"Location: {reminder.location}"
            f"Event datetime: {reminder.execute_at}",
            settings.EMAIL_HOST_USER,
            recipients,
            fail_silently=False,
        )
        reminder.is_done = True
        reminder.save()
    logging.info("End celery send_mailings task")
