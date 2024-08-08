from account.authentication import EmailAuthBackend
from tests.base_test import *


class EmailAuthBackendTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.backend = EmailAuthBackend()

    def test_authenticate_with_valid_email(self):
        user = self.backend.authenticate(
            request=None, username=self.existing_email, password=self.password
        )
        self.assertIsNotNone(user)

    def test_authenticate_with_invalid_email(self):
        user = self.backend.authenticate(
            request=None, username=self.invalid_email, password=self.password
        )
        self.assertIsNone(user)

    def test_authenticate_with_valid_username(self):
        user = self.backend.authenticate(
            None, username=self.existing_user, password=self.password
        )
        self.assertIsNotNone(user)

    def test_authenticate_with_invalid_username(self):
        user = self.backend.authenticate(
            None, username="unknown", password=self.password
        )
        self.assertIsNone(user)

    def test_authenticate_with_multiple_users(self):
        Profile.objects.create_user(
            username="anotheruser", email=self.existing_email, password=self.password
        )
        user = self.backend.authenticate(
            None, username=self.existing_email, password=self.password
        )
        self.assertIsNone(user)

    def test_authenticate_with_invalid_password(self):
        user = self.backend.authenticate(
            request=None, username=self.existing_email, password="wrongpass"
        )
        self.assertIsNone(user)

    def test_get_user_with_valid_id(self):
        user = Profile.objects.get(username=self.existing_user)
        fetched_user = self.backend.get_user(user.id)
        self.assertEqual(fetched_user, user)

    def test_get_user_with_invalid_id(self):
        fetched_user = self.backend.get_user(999)
        self.assertIsNone(fetched_user)
