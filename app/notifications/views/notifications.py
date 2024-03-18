from app.base.permissions import IsOwnerOrReadOnly
from app.base.views import CDLUViewSet

from ..models import Notification
from ..serializers import NotificationSerializer

__all__ = ["NotificationViewSet"]


class NotificationViewSet(CDLUViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsOwnerOrReadOnly,)
