from rest_framework.permissions import IsAuthenticated

from app.base.filters import IsBelongNotificationFilterBackend
from app.base.views import CDLUViewSet
from app.base.permissions import IsOwnerOrReadOnly

from ..models import Notification
from ..serializers import NotificationSerializer

__all__ = ["NotificationViewSet"]


class NotificationViewSet(CDLUViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (IsBelongNotificationFilterBackend,)
