import random
from copy import copy

import factory
from django.urls import reverse
from parameterized import parameterized
from rest_framework_simplejwt.tokens import RefreshToken

from .base import BaseTestCase
from .factories import UserLoginFactory
from .utils import get_api_client, get_user


class AuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = UserLoginFactory
        self.url = reverse("rest_login")
        self.user_data = factory.build(dict, FACTORY_CLASS=self.factory)

    def test_login_successful(self):
        self.user = get_user(**self.user_data)
        response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(len(response.data.get("user")), 5)

    def test_login_email_failed(self):
        self.user = get_user(**self.user_data)
        user_data = copy(self.user_data)
        user_data["username"] = f"{random.randint(1000, 9999)}{self.user_data.get('username')}"
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

        user_data = copy(self.user_data)
        user_data["password"] = f"{random.randint(1000, 9999)}{self.user_data.get('password')}"
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([({}, 400), ({"username": ""}, 400)])
    def test_login_not_valid_email(self, user_data, code):
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, code)

    def test_login_not_valid_password(self):
        user_data = copy(self.user_data)
        del user_data["username"]
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

        user_data = copy(self.user_data)
        user_data["password"] = ""
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

        user_data = copy(self.user_data)
        user_data["password"] = "123"
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

        user_data = copy(self.user_data)
        user_data["password"] = "12345678"
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

        user_data = copy(self.user_data)
        user_data["password"] = "Sojdlg123aljg"
        response = self.client.post(self.url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_logout_successful(self):
        self.user = get_user(**self.user_data)
        login_response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(login_response.status_code, 200)

        logout_response = self.client.post(
            reverse("rest_logout"), {"refresh": login_response.data.get("refresh")}, format="json"
        )
        self.assertEqual(logout_response.status_code, 200)

    def test_get_user_data_jwt_successful(self):
        self.user = get_user(**self.user_data)
        access = str(RefreshToken.for_user(self.user).access_token)
        api_client = get_api_client(access)

        user_details_response = api_client.get(reverse("rest_user_details"), format="json")
        self.assertEqual(user_details_response.status_code, 200)

    def test_get_user_data_without_jwt_failed(self):
        self.user = get_user(**self.user_data)
        login_response = self.client.get(reverse("rest_user_details"), format="json")
        self.assertEqual(login_response.status_code, 401)

    def test_get_user_data_refresh_blacklist_jwt(self):
        self.user = get_user(**self.user_data)
        login_response = self.client.post(self.url, self.user_data, format="json")
        self.assertEqual(login_response.status_code, 200)

        api_client = get_api_client(login_response.data.get("access"))

        user_details_response = api_client.get(reverse("rest_user_details"), format="json")
        self.assertEqual(user_details_response.status_code, 200)

        refresh_data = {"refresh": login_response.data.get("refresh")}
        logout_response = self.client.post(reverse("rest_logout"), refresh_data, format="json")
        self.assertEqual(logout_response.status_code, 200)

        token_data = {"token": login_response.data.get("refresh")}
        user_details_response = self.client.post(reverse("token_verify"), token_data, format="json")
        self.assertEqual(user_details_response.status_code, 400)

        user_details_response = self.client.post(reverse("token_refresh"), refresh_data, format="json")
        self.assertEqual(user_details_response.status_code, 401)
