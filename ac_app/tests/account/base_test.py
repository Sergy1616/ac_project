from django.contrib.auth import get_user_model
from django.test import TestCase, Client

Profile = get_user_model()


class BaseTest(TestCase):
    fixtures = ["ac_app_data.json"]

    def setUp(self):
        self.existing_user = "existinguser"
        self.existing_email = "existinguser@mail.com"
        self.password = "testpass123"

        self.username = "testuser"
        self.email = "testuser@mail.com"
        self.invalid_email = "invalid_email.com"

        self.user = Profile.objects.create_user(
            username=self.existing_user,
            email=self.existing_email,
            password=self.password,
        )

    def get_test_form_data(self, **kwargs):
        default_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }
        default_data.update(kwargs)
        return default_data
