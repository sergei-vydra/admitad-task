from django.db import models
from django.contrib.auth import get_user_model

__all__ = ["Notification"]


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="notifications")
    recipients = models.ManyToManyField(get_user_model())
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(blank=True, default="")
    location = models.CharField(blank=True, default="")
    is_done = models.BooleanField(default=False)
    execute_at = models.DateTimeField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
