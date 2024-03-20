from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.base.filters import IsBelongNotificationFilterBackend
from app.base.permissions import IsOwnerOrReadOnly

from ..models import Notification
from ..serializers import NotificationSerializer

__all__ = ["NotificationViewSet", "NotificationOwnerListAPI", "NotificationParticipantListAPI"]


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (IsBelongNotificationFilterBackend,)


class NotificationOwnerListAPI(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationParticipantListAPI(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(recipients__in=[self.request.user])
