from django.urls import include, path

urlpatterns = [
    path("users/", include("app.users.urls")),
    path("reminders/", include("app.reminders.urls")),
]
