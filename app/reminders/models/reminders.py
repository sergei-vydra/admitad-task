from django.contrib.auth import get_user_model
from django.db import models

__all__ = ["Reminder"]


class Reminder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="reminders")
    recipients = models.ManyToManyField(get_user_model())
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    is_done = models.BooleanField(default=False)
    execute_at = models.DateTimeField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Reminder"
        verbose_name_plural = "Reminders"
