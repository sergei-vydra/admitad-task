from dj_rest_auth.registration.views import VerifyEmailView as BaseVerifyEmailView
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.views import LogoutView as BaseLogoutView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers import LogoutSerializer

__all__ = ["LogoutView", "VerifyEmailView", "UserListAPI"]


class LogoutView(BaseLogoutView):
    http_method_names = ["post"]
    serializer_class = LogoutSerializer

    @extend_schema(
        request=LogoutSerializer,
        responses={
            200: inline_serializer(name="LogoutResponse", fields={"detail": serializers.CharField()}),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VerifyEmailView(BaseVerifyEmailView):
    allowed_methods = ("POST", "OPTIONS", "HEAD", "GET")

    def get(self, request, key, *args, **kwargs):
        self.kwargs["key"] = key
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({"detail": _("ok")}, status=status.HTTP_200_OK)


class UserListAPI(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_user_model().objects.filter(is_active=True)
