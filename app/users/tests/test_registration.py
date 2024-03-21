import random

import factory
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from parameterized import parameterized

from .base import BaseTestCase
from .factories import UserLoginFactory


@override_settings(EMAIL_HOST=None)
class RegistrationTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = UserLoginFactory
        self.url = reverse("rest_register")

    def test_registration_successful(self):
        before_user_count = get_user_model().objects.all().count()
        before_user_account_count = EmailAddress.objects.all().count()

        registration_data = factory.build(dict, FACTORY_CLASS=self.factory)
        registration_data["password1"] = registration_data.get("password")
        registration_data["password2"] = registration_data.get("password")
        response = self.client.post(self.url, registration_data, format="json")
        self.assertEqual(response.status_code, 201)

        self.assertEqual(get_user_model().objects.count(), before_user_count + 1)
        self.assertEqual(EmailAddress.objects.count(), before_user_account_count + 1)
        user = get_user_model().objects.get(email=registration_data.get("email"))
        self.assertEqual(user.id, get_user_model().objects.latest("id").id)
        self.assertEqual(user.email, registration_data.get("email"))

        registration_data["email"] = f"{random.randint(1000, 9999)}{registration_data.get('email')}"
        registration_data["username"] = f"{random.randint(1000, 9999)}{registration_data.get('username')}"
        response2 = self.client.post(self.url, registration_data, format="json")
        self.assertEqual(response2.status_code, 201)
        user2 = get_user_model().objects.get(email=registration_data.get("email"))
        self.assertNotEqual(user.id, user2.id)

    @parameterized.expand(
        [
            ({"email": "@gmail", "name": "name"},),
            ({"email": "@gmail.com", "name": "name"},),
            ({"email": "john_dore", "name": "name"},),
            ({"email": "john_dore@", "name": "name"},),
            ({"email": "john_dore@gmail", "name": "name"},),
        ]
    )
    def test_registration_not_valid_email(self, registration_data: dict[str, str]):
        response = self.client.post(self.url, registration_data, format="json")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand(
        [
            ({"email": "john_dore@gmail.com"},),
            ({"email": "john_dore@gmail.com", "username": "username"},),
            ({"mail": "john_dore@gmail.com", "username": "username"},),
            ({},),
        ]
    )
    def test_registration_not_valid_body(self, registration_data: dict[str, str]):
        response = self.client.post(self.url, registration_data, format="json")
        self.assertEqual(response.status_code, 400)


@override_settings(EMAIL_HOST=None)
class RegistrationResendEmailTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = UserLoginFactory
        self.url = reverse("rest_resend_email")

    def test_resend_email_successful(self):
        registration_data = factory.build(dict, FACTORY_CLASS=self.factory)
        if get_user_model().objects.filter(email=registration_data.get("email")).first():
            registration_data["email"] = f"{random.randint(1000, 9999)}{registration_data.get('email')}"
        user = get_user_model().objects.create(**registration_data)
        before_user_count = get_user_model().objects.count()
        response = self.client.post(self.url, {"email": registration_data.get("email")}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(before_user_count, get_user_model().objects.count())
        self.assertEqual(user, get_user_model().objects.filter(email=registration_data.get("email")).first())

    @parameterized.expand(
        [
            ({"email": "@gmail"},),
            ({"email": "@gmail.com"},),
            ({"email": "john_dore"},),
            ({"email": "john_dore@"},),
            ({"email": "john_dore@gmail"},),
        ]
    )
    def test_registration_not_valid_email(self, registration_data: dict[str, str]):
        response = self.client.post(self.url, registration_data, format="json")
        self.assertEqual(response.status_code, 400)

    @parameterized.expand(
        [
            ({"mail": "john_dore@gmail.com"},),
            ({},),
        ]
    )
    def test_registration_not_valid_body(self, registration_data: dict[str, str]):
        response = self.client.post(self.url, registration_data, format="json")
        self.assertEqual(response.status_code, 400)
