from django.contrib import admin
from django.contrib.admin import ModelAdmin

from app.reminders.models import Reminder

__all__ = ["ReminderAdmin"]


@admin.register(Reminder)
class ReminderAdmin(ModelAdmin):
    list_filter = ("title",)
    list_display = ("title", "user", "execute_at")
    ordering = ("user",)
