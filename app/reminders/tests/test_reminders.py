import factory
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from app.users.tests.factories import UserLoginFactory
from app.users.tests.utils import get_api_client, get_user

from ..models import Reminder
from .base import BaseTestCase
from .factories import PayoutRequestFactory


class ReminderTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("reminder-list")
        self.user_data = factory.build(dict, FACTORY_CLASS=UserLoginFactory)
        self.factory = PayoutRequestFactory
        self.user = get_user(**self.user_data)
        self.access = str(RefreshToken.for_user(self.user).access_token)
        self.api_client = get_api_client(self.access)

    def get_reminder_data(self):
        reminder_data = factory.build(dict, FACTORY_CLASS=self.factory)
        del reminder_data["user"]
        reminder_data["recipients"] = [self.user.pk]
        return reminder_data

    def test_get_reminders_failed(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 401)

    def test_update_reminders_failed(self):
        reminder_data = self.get_reminder_data()
        response = self.api_client.post(f"{self.url}", reminder_data, format="json")
        reminder_id = response.data.get("id")
        response = self.client.patch(f"{self.url}{reminder_id}/", {"location": "Location"}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_delete_reminders_failed(self):
        reminder_data = self.get_reminder_data()
        response = self.api_client.post(f"{self.url}", reminder_data, format="json")
        reminder_id = response.data.get("id")
        response = self.client.delete(f"{self.url}{reminder_id}/", format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_reminder_successful(self):
        reminder_data = self.get_reminder_data()
        response = self.api_client.post(self.url, reminder_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertIn("is_done", response.data)
        self.assertNotIn("user", response.data)
        self.assertEqual(len(response.data), 7)

    def test_get_reminders_successful(self):
        reminder_data = self.get_reminder_data()
        response_post = self.api_client.post(self.url, reminder_data, format="json")
        response_get = self.api_client.get(self.url, format="json")
        self.assertEqual(response_get.status_code, 200)
        self.assertIn("count", response_get.data)
        self.assertIn("results", response_get.data)
        self.assertEqual(len(response_get.data.get("results")), response_get.data.get("count"))
        self.assertEqual(response_get.data.get("results")[0].get("id"), response_post.data.get("id"))

    def test_update_reminders_successful(self):
        reminder_data = self.get_reminder_data()
        response = self.api_client.post(self.url, reminder_data, format="json")
        reminder_id = response.data.get("id")
        new_location = self.faker.city()
        response = self.api_client.patch(f"{self.url}{reminder_id}/", {"location": new_location}, format="json")
        reminder = Reminder.objects.get(pk=reminder_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_location, reminder.location)

    def test_delete_reminders_successful(self):
        before_count = Reminder.objects.count()
        reminder_data = self.get_reminder_data()
        response = self.api_client.post(f"{self.url}", reminder_data, format="json")
        reminder_count = Reminder.objects.count()
        self.assertEqual(before_count + 1, reminder_count)
        reminder_id = response.data.get("id")
        response = self.api_client.delete(f"{self.url}{reminder_id}/", format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(reminder_count - 1, Reminder.objects.count())


class ReminderOwnTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("reminder-own")
        self.user_data = factory.build(dict, FACTORY_CLASS=UserLoginFactory)
        self.factory = PayoutRequestFactory
        self.user = get_user(**self.user_data)
        self.access = str(RefreshToken.for_user(self.user).access_token)
        self.api_client = get_api_client(self.access)

    def get_reminder_data(self):
        reminder_data = factory.build(dict, FACTORY_CLASS=self.factory)
        del reminder_data["user"]
        reminder_data["recipients"] = [self.user.pk]
        return reminder_data

    def test_get_reminders_failed(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_reminders_successful(self):
        reminder_data = self.get_reminder_data()
        self.api_client.post(reverse("reminder-list"), reminder_data, format="json")
        response_get = self.api_client.get(self.url, format="json")
        self.assertEqual(response_get.status_code, 200)
        self.assertIn("count", response_get.data)
        self.assertIn("results", response_get.data)
        self.assertEqual(len(response_get.data.get("results")), response_get.data.get("count"))
        self.assertNotEqual(response_get.data.get("count"), 0)

        user2 = get_user(**factory.build(dict, FACTORY_CLASS=UserLoginFactory))
        access2 = str(RefreshToken.for_user(user2).access_token)
        api_client2 = get_api_client(access2)
        response_get2 = api_client2.get(self.url, format="json")
        self.assertEqual(response_get2.status_code, 200)
        self.assertIn("count", response_get2.data)
        self.assertIn("results", response_get2.data)
        self.assertEqual(len(response_get2.data.get("results")), response_get2.data.get("count"))
        self.assertEqual(response_get2.data.get("count"), 0)


class ReminderParticipantTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("reminder-consist")
        self.user_data = factory.build(dict, FACTORY_CLASS=UserLoginFactory)
        self.factory = PayoutRequestFactory
        self.user = get_user(**self.user_data)
        self.access = str(RefreshToken.for_user(self.user).access_token)
        self.api_client = get_api_client(self.access)

    def get_reminder_data(self, recipients: list) -> dict:
        reminder_data = factory.build(dict, FACTORY_CLASS=self.factory)
        del reminder_data["user"]
        reminder_data["recipients"] = recipients
        return reminder_data

    def test_get_reminders_failed(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_reminders_successful(self):
        user2 = get_user(**factory.build(dict, FACTORY_CLASS=UserLoginFactory))
        access2 = str(RefreshToken.for_user(user2).access_token)
        api_client2 = get_api_client(access2)
        response_get2 = api_client2.get(self.url, format="json")

        self.assertEqual(response_get2.status_code, 200)
        self.assertIn("count", response_get2.data)
        self.assertIn("results", response_get2.data)
        self.assertEqual(len(response_get2.data.get("results")), response_get2.data.get("count"))
        self.assertEqual(response_get2.data.get("count"), 0)

        reminder_data = self.get_reminder_data([user2.pk])
        self.api_client.post(reverse("reminder-list"), reminder_data, format="json")

        response_get3 = api_client2.get(self.url, format="json")
        self.assertEqual(response_get3.status_code, 200)
        self.assertIn("count", response_get3.data)
        self.assertIn("results", response_get3.data)
        self.assertEqual(len(response_get3.data.get("results")), response_get3.data.get("count"))
        self.assertNotEqual(response_get3.data.get("count"), 0)

        response_get1 = self.api_client.get(self.url, format="json")
        self.assertEqual(response_get1.status_code, 200)
        self.assertEqual(response_get2.data.get("count"), 0)
