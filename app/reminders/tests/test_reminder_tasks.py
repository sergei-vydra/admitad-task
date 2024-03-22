import factory
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from app.users.tests.factories import UserLoginFactory
from app.users.tests.utils import get_api_client, get_user

from ..tasks import send_mailings
from .base import BaseTestCase
from .factories import PayoutRequestFactory


@override_settings(EMAIL_HOST=None)
class SendMailingsTaskTestCase(BaseTestCase):
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

    def test_apply_send_mailings_successfully(self):
        reminder_data = self.get_reminder_data()
        reminder_data["executed_at"] = timezone.now()
        self.api_client.post(self.url, reminder_data, format="json")
        task = send_mailings.s().apply()
        self.assertEqual(task.state, "SUCCESS")
