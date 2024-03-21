from dj_rest_auth.serializers import LoginSerializer as DjRestLoginSerializer
from rest_framework import serializers

__all__ = ["LoginSerializer", "LogoutSerializer"]


class LoginSerializer(DjRestLoginSerializer):
    email = None


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
