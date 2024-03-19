from rest_framework import serializers

from ..models import Notification

__all__ = ["NotificationSerializer"]


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        recipients = validated_data.pop("recipients")
        notification = Notification.objects.create(**validated_data)
        notification.recipients.set(recipients)
        return notification

    class Meta:
        model = Notification
        exclude = ("is_done", "created_at")
