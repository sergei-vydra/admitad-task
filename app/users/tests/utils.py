from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AuthUser


def get_user(username: str, email: str, password: str) -> AuthUser:
    user = get_user_model().objects.create_user(username=username, email=email, password=password)
    user.emailaddress_set.create(user=user, email=user.email, verified=True)
    return user


def get_api_client(access_token: str) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client
