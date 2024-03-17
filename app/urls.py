from django.urls import include, path

urlpatterns = [
    path("users/", include("app.users.urls")),
]
