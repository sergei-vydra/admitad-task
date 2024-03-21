from factory.faker import faker
from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    def setUp(self):
        self.faker = faker.Faker()
