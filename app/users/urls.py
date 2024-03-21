from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import include, path, re_path

from .views.users import LogoutView, UserListAPI, VerifyEmailView

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path(
        "password/reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"
    ),
    path("", include("dj_rest_auth.urls")),
    re_path(
        r"^registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("", UserListAPI.as_view(), name="users"),
]
