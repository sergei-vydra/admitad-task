from django.urls import include, path

urlpatterns = [
    path("users/", include("app.users.urls")),
    path("notifications/", include("app.notifications.urls")),
]
