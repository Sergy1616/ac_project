from tests.base_test import *
from account.forms import (
    SignUpProfileForm,
    ProfileEditForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    DeleteAccountForm,
)


class SignUpProfileFormTest(BaseTest):
    def test_valid_form(self):
        form_data = self.get_test_form_data()
        form = SignUpProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_existing_email(self):
        form_data = self.get_test_form_data(email=self.existing_email)
        form = SignUpProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Email already in use.", form.errors["email"])

    def test_short_username(self):
        form_data = self.get_test_form_data(username="user")
        form = SignUpProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Ensure this value has at least 5 characters (it has 4).",
            form.errors["username"],
        )


class ProfileEditFormTest(BaseTest):
    def test_valid_form(self):
        form_data = {
            "photo": "test.jpg",
            "remove_photo": False,
            "username": self.username,
            "first_name": "Test",
            "last_name": "User",
            "email": self.email,
            "bio": "Test bio",
        }
        form = ProfileEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form_existing_username(self):
        form_data = {"username": self.existing_user}
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "A user with that username already exists.", form.errors["username"]
        )
        self.assertIn("username", form.errors)

    def test_invalid_form_existing_email(self):
        form_data = {
            "username": self.username,
            "email": self.existing_email,
        }
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("", form.errors["email"][0])
        self.assertEqual(form.errors["email"][0], " Email already in use.")
        self.assertIn("email", form.errors)

    def test_short_username(self):
        form_data = {"username": "test"}
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Ensure this value has at least 5 characters (it has 4).",
            form.errors["username"],
        )


class CustomPasswordChangeFormTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.new_password = "newpass123"
        self.user_without_password = Profile.objects.create_user(
            username=self.username, email=self.email
        )
        self.user_without_password.set_unusable_password()
        self.user_without_password.save()

    def test_form_with_usable_password(self):
        form_data = {
            "old_password": self.password,
            "new_password1": self.new_password,
            "new_password2": self.new_password,
        }
        form = CustomPasswordChangeForm(self.user, form_data)
        self.assertIn("old_password", form.fields)
        self.assertTrue(form.is_valid())

    def test_form_without_old_password(self):
        form_data = {
            "new_password1": self.new_password,
            "new_password2": self.new_password,
        }
        form = CustomPasswordChangeForm(self.user_without_password, form_data)
        self.assertNotIn("old_password", form.fields)
        self.assertTrue(form.is_valid())


class CustomPasswordResetFormTest(BaseTest):
    def test_form_valid_email(self):
        form = CustomPasswordResetForm(data={"email": self.existing_email})
        self.assertTrue(form.is_valid())

    def test_form_invalid_email_not_found(self):
        form = CustomPasswordResetForm(data={"email": "nonexistent@example.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"][0], "No account found with that email address."
        )

    def test_invalid_email_format(self):
        form = CustomPasswordResetForm(data={"email": self.invalid_email})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_case_insensitivity(self):
        form = CustomPasswordResetForm(data={"email": "ExIsTiNgUsEr@MaIl.Com"})
        self.assertTrue(form.is_valid())

    def test_empty_email(self):
        form = CustomPasswordResetForm(data={"email": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_whitespace_email(self):
        form = CustomPasswordResetForm(data={"email": " "})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"][0], "This field is required.")


class DeleteAccountFormTest(BaseTest):
    def test_delete_account_form_valid(self):
        form_data = {"password": self.password, "confirm_delete": True}
        form = DeleteAccountForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_delete_account_form_invalid_password_missing(self):
        form_data = {"password": "", "confirm_delete": True}
        form = DeleteAccountForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_delete_account_form_invalid_confirm_delete_missing(self):
        form_data = {"password": self.password, "confirm_delete": False}
        form = DeleteAccountForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("confirm_delete", form.errors)
