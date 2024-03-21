from rest_framework import serializers

from ..models import Reminder

__all__ = ["ReminderSerializer"]


class ReminderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_done = serializers.BooleanField(default=False)

    def create(self, validated_data):
        recipients = validated_data.pop("recipients")
        reminder = Reminder.objects.create(**validated_data)
        reminder.recipients.set(recipients)
        return reminder

    class Meta:
        model = Reminder
        exclude = ("created_at",)
