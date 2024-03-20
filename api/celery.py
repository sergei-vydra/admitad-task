import os
from datetime import timedelta

from celery import Celery

from api import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
app = Celery(
    "api",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    broker_connection_retry_on_startup=True,
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_SOFT_TIME_LIMIT = 3540
CELERY_TASK_TIME_LIMIT = 3600
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_ACKS_LATE = True

app.conf.beat_schedule = {
    "run-every-1-minute": {
        "task": "app.notifications.tasks.notification_tasks.send_mailings",
        "schedule": timedelta(minutes=1),
    },
}
