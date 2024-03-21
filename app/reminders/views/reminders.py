from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.base.filters import IsBelongReminderFilterBackend
from app.base.permissions import IsOwnerOrReadOnly

from ..models import Reminder
from ..serializers import ReminderSerializer

__all__ = ["ReminderViewSet", "ReminderOwnerListAPI", "ReminderParticipantListAPI"]


class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (IsBelongReminderFilterBackend,)


class ReminderOwnerListAPI(ListAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user, is_done=False)


class ReminderParticipantListAPI(ListAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reminder.objects.filter(recipients__in=[self.request.user], is_done=False)
