import random

import factory
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from parameterized import parameterized

from ..models import UserAccount
from ..views.dj_rest_views import ResendEmailVerificationView, VerifyEmailView
from .base import BaseTestCase
from .factories import TestRegistrationFactory


@override_settings(EMAIL_HOST=None)
class RegistrationTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = TestRegistrationFactory
        self.url = reverse("rest_register")
        RegisterView.throttle_classes = []

    def test_registration_successful(self):
        before_user_count = get_user_model().objects.all().count()
        before_user_account_count = UserAccount.objects.all().count()

        registration_data = factory.build(dict, FACTORY_CLASS=self.factory)
        response = self.client.post(self.url, registration_data, format="json")
        self.assertEqual(response.status_code, 201)

        self.assertEqual(get_user_model().objects.count(), before_user_count + 1)
        self.assertEqual(UserAccount.objects.count(), before_user_account_count + 1)
        user = get_user_model().objects.get(email=registration_data.get("email"))
        self.assertEqual(user.id, get_user_model().objects.latest("id").id)
        self.assertEqual(user.email, registration_data.get("email"))
        self.assertEqual(user.name, registration_data.get("name"))

        registration_data["email"] = f"{random.randint(1000, 9999)}{registration_data.get('email')}"
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
            ({"email": "john_dore@gmail.com", "first_name": "Some name"},),
            ({"mail": "john_dore@gmail.com", "name": "Some name"},),
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
        self.factory = TestRegistrationFactory
        self.url = reverse("rest_resend_email")
        ResendEmailVerificationView.throttle_classes = []

    def test_resend_email_successful(self):
        registration_data = factory.build(dict, FACTORY_CLASS=TestRegistrationFactory)
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


@override_settings(EMAIL_HOST=None)
class RegistrationVerifyEmailTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = TestRegistrationFactory
        self.url = reverse("rest_verify_email")
        VerifyEmailView.throttle_classes = []

    def get_email_confirmation(self):
        registration_data = factory.build(dict, FACTORY_CLASS=self.factory)
        self.client.post(reverse("rest_register"), registration_data, format="json")
        user = get_user_model().objects.filter(email=registration_data.get("email"))[0]

        return user.emailaddress_set.get(email=registration_data.get("email")).emailconfirmation_set.order_by(
            "-created"
        )[0]

    def test_verify_email_successful(self):
        email_confirmation = self.get_email_confirmation()
        password = self.faker.password()
        response = self.client.post(
            self.url,
            {"key": email_confirmation.key, "password": password, "password_confirm": password},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_verify_email_not_valid_key(self):
        password = self.faker.password()

        response = self.client.post(
            self.url,
            {"key": password, "password": password, "password_confirm": password},
            format="json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("user", response.data)

        response = self.client.post(
            self.url,
            {"key": "", "password": password, "password_confirm": password},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("user", response.data)

        response = self.client.post(
            self.url,
            {"password": password, "password_confirm": password},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("user", response.data)

    def test_verify_email_not_valid_password(self):
        email_confirmation = self.get_email_confirmation()
        password = self.faker.password()

        response = self.client.post(
            self.url,
            {"key": email_confirmation.key, "password": password, "password_confirm": f"not_{password}"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("user", response.data)

        response = self.client.post(self.url, {"key": email_confirmation.key, "password": password}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("user", response.data)

        response = self.client.post(
            self.url, {"key": email_confirmation.key, "password_confirm": password}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("user", response.data)

        response = self.client.post(self.url, {"key": email_confirmation.key}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("user", response.data)
