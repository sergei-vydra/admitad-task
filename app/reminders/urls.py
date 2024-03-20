from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ReminderOwnerListAPI, ReminderParticipantListAPI, ReminderViewSet

router = DefaultRouter()
router.register("", ReminderViewSet)

urlpatterns = [
    path("own", ReminderOwnerListAPI.as_view(), name="reminder-own"),
    path("consist", ReminderParticipantListAPI.as_view(), name="reminder-consist"),
]

urlpatterns += router.urls
