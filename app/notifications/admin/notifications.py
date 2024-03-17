from django.contrib import admin
from django.contrib.admin import ModelAdmin

from app.notifications.models import Notification

__all__ = ["NotificationAdmin"]


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_filter = ("title",)
    list_display = ("title", "user", "execute_at")
    ordering = ("user",)
