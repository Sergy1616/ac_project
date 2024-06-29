from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse

from account.models import upload_photo
from account.validators import validate_file_size


class ProfileModelTest(TestCase):
    def setUp(self):
        self.Profile = get_user_model()
        self.username = "testuser"
        self.email = "testuser@mail.com"
        self.password = "testpass123"
        self.test_image = SimpleUploadedFile(
            name="test_image.jpg", content=b"content", content_type="image/jpeg"
        )
        self.bio = "Test bio"

    def create_user(self, **kwargs):
        default_data = {"username": self.username, "password": self.password}
        default_data.update(kwargs)
        return self.Profile.objects.create_user(**default_data)

    def test_str_method(self):
        user = self.create_user()
        self.assertEqual(str(user), "testuser")

    def test_get_absolute_url_method(self):
        user = self.create_user()
        expected_url = reverse("user_detail", kwargs={"username": user.username})
        self.assertEqual(user.get_absolute_url(), expected_url)

    def test_username_and_email_saved_as_lower(self):
        user = self.Profile.objects.create_user(
            username="TestUser",
            email="TEST@EXAMPLE.COM",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

    def test_create_profile_without_photo_and_bio(self):
        user = self.create_user()
        self.assertEqual(user.username, "testuser")
        self.assertFalse(user.photo)
        self.assertEqual(user.bio, "")

    def test_create_profile_with_photo_and_bio(self):
        user = self.create_user(photo=self.test_image, bio=self.bio)
        self.assertIsNotNone(user.photo)
        expected_upload_path = f"users/{user.username}/{self.test_image}"
        self.assertEqual(upload_photo(user, "test_image.jpg"), expected_upload_path)
        self.assertEqual(user.bio, "Test bio")

        user.photo.delete()


class ValidateFileSizeTestCase(TestCase):
    def test_file_size_under_limit(self):
        small_file = SimpleUploadedFile("small_file.txt", b"x" * 512 * 1024)
        try:
            validate_file_size(small_file)
        except ValidationError:
            self.fail("validate_file_size() raised ValidationError unexpectedly!")

    def test_file_size_over_limit(self):
        large_file = SimpleUploadedFile("large_file.txt", b"x" * 2 * 1024 * 1024)

        with self.assertRaises(ValidationError) as context:
            validate_file_size(large_file)
        self.assertIn(
            "The maximum file size that can be uploaded is 1 MB",
            context.exception.messages,
        )

    def test_file_size_exactly_limit(self):
        exact_file = SimpleUploadedFile("exact_file.txt", b"x" * 1024 * 1024)
        try:
            validate_file_size(exact_file)
        except ValidationError:
            self.fail("validate_file_size() raised ValidationError unexpectedly!")
