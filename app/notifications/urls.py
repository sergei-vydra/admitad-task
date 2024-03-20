from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import NotificationOwnerListAPI, NotificationParticipantListAPI, NotificationViewSet

router = DefaultRouter()
router.register("", NotificationViewSet)

urlpatterns = [
    path("own", NotificationOwnerListAPI.as_view(), name="notification-own"),
    path("consist", NotificationParticipantListAPI.as_view(), name="notification-consist"),
]

urlpatterns += router.urls
