import factory
import pytz
from factory.django import DjangoModelFactory

from app.users.tests.factories import UserRegistrationFactory

from ..models import Reminder


class PayoutRequestFactory(DjangoModelFactory):
    class Meta:
        model = Reminder

    user = factory.SubFactory(UserRegistrationFactory)
    title = factory.Faker("name")
    description = factory.Faker("text")
    location = factory.Faker("city")
    is_done = False
    execute_at = factory.Faker("date_time_between", start_date="now", end_date="+10d", tzinfo=pytz.UTC)
    created_at = factory.Faker("date_time_between", start_date="-10d", end_date="now", tzinfo=pytz.UTC)

    @factory.post_generation
    def recipients(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.recipients.add(*extracted)
