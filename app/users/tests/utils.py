from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AuthUser


def get_user(email: str, password: str) -> AuthUser:
    return get_user_model().objects.create_user(email=email, password=password)


def get_api_client(access_token: str) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client
