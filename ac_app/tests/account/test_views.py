from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, resolve
from django.utils.text import slugify

from cart.forms import CartAddProductForm
from shop.models import WishList, Product
from space.models import Comment, FavoriteStar, Star
from tests.base_test import *
from account.forms import (
    SignUpProfileForm,
    ProfileEditForm,
    CustomPasswordResetForm,
    CustomPasswordChangeForm,
    DeleteAccountForm,
)
from account.views import (
    ProfileView,
    SignUpProfileView,
    EditProfileView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    DeleteAccountView,
    UserCommentsView,
    UserFavoriteStarsView,
    UserWishListView,
)


class AjaxHtmxValidationTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_X_REQUESTED_WITH="XMLHttpRequest")

    def test_check_username_success(self):
        response = self.client.post(
            reverse("check-user"), {"username_or_email": self.existing_user}
        )
        self.assertContains(response, '<div class="login-success"></div>')

    def test_check_email_success(self):
        response = self.client.post(
            reverse("check-user"), {"username_or_email": self.existing_email}
        )
        self.assertContains(response, '<div class="login-success"></div>')

    def test_check_username_fail(self):
        response = self.client.post(
            reverse("check-user"), {"username_or_email": "nonexistent_user"}
        )
        self.assertContains(response, "No user with this username exists")

    def test_check_email_fail(self):
        response = self.client.post(
            reverse("check-user"), {"username_or_email": "nonexistent@email.com"}
        )
        self.assertContains(response, "No user with this email exists")

    def test_check_password_success(self):
        response = self.client.post(
            reverse("check-password"),
            {"username_or_email": self.existing_user, "password": self.password},
        )
        self.assertContains(response, '<div class="password-success"></div>')

    def test_check_password_fail(self):
        response = self.client.post(
            reverse("check-password"),
            {"username_or_email": self.existing_user, "password": "wrongpass"},
        )
        self.assertContains(response, "Incorrect password")

    def test_check_password_user_not_found(self):
        response = self.client.post(
            reverse("check-password"),
            {"username_or_email": "nonexistent_user", "password": self.password},
        )
        self.assertContains(response, "No user with this username or email exists")

    def test_check_password_short(self):
        response = self.client.post(
            reverse("check-password"),
            {"username_or_email": self.existing_user, "password": "short"},
        )
        self.assertContains(
            response, "Your password must be at least 8 characters long"
        )

    def test_login_user_htmx_success(self):
        response = self.client.post(
            reverse("login_user"),
            {"username_or_email": self.existing_user, "password": self.password},
        )
        self.assertJSONEqual(
            response.content, {"message": f"Welcome {self.existing_user}!"}
        )
        self.assertEqual(response["HX-Trigger"], "loginSuccess")
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_user_htmx_invalid_password(self):
        response = self.client.post(
            reverse("login_user"),
            {"username_or_email": self.existing_user, "password": "wrongpass"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.content.decode())
        self.assertContains(response, "Invalid username or password", status_code=401)

    def test_login_user_htmx_invalid_user(self):
        response = self.client.post(
            reverse("login_user"),
            {"username_or_email": self.invalid_email, "password": self.password},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.content.decode())

    def test_login_user_htmx_user_not_found(self):
        response = self.client.post(
            reverse("login_user"),
            {"username_or_email": "nonexistent_user", "password": self.password},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.content.decode())


class ProfileViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.existing_user, password=self.password)
        self.url = reverse("user_detail", kwargs={"username": self.user.username})
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/{}/".format(self.user.username))
        self.assertEqual(view.func.__name__, ProfileView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "account/profile.html")
        self.assertEqual(self.response.context["profile"], self.user)

    def test_unauthenticated_user_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, "/account/login/?next={}".format(self.url))


class SignUpProfileViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("signup")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/signup/")
        self.assertEqual(view.func.__name__, SignUpProfileView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "registration/signup.html")
        self.assertIsInstance(self.response.context["signup_form"], SignUpProfileForm)
        self.assertIsInstance(self.response.context["login_form"], AuthenticationForm)

    def test_form_valid(self):
        form_data = self.get_test_form_data()
        response = self.client.post(self.url, form_data)
        self.assertTrue(Profile.objects.filter(username=self.username).exists())
        new_user = Profile.objects.get(username=self.username)
        self.assertRedirects(
            response, reverse("user_detail", kwargs={"username": new_user.username})
        )

    def test_form_invalid(self):
        form_data = self.get_test_form_data(
            username="test",
            email=self.invalid_email,
            password2="differentpassword",
        )
        response = self.client.post(self.url, form_data)
        self.assertFormError(
            response,
            "signup_form",
            "username",
            "Ensure this value has at least 5 characters (it has 4).",
        )
        self.assertFormError(
            response, "signup_form", "email", "Enter a valid email address."
        )
        self.assertFormError(
            response,
            "signup_form",
            "password2",
            "The two password fields didn’t match.",
        )

    def test_email_already_used(self):
        form_data = self.get_test_form_data(email=self.existing_email)
        response = self.client.post(self.url, form_data)
        self.assertFormError(response, "signup_form", "email", "Email already in use.")


class EditProfileViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse("edit_profile")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/edit/")
        self.assertEqual(view.func.__name__, EditProfileView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "account/edit_profile.html")
        self.assertIsInstance(self.response.context["form"], ProfileEditForm)

    def test_form_valid(self):
        form_data = {
            "photo": "test.jpg",
            "remove_photo": False,
            "username": self.username,
            "first_name": "Test",
            "last_name": "User",
            "email": self.email,
            "bio": "Test bio",
        }
        response = self.client.post(self.url, form_data, HTTP_REFERER=self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(username=self.username).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(message) == "Your profile has been updated." for message in messages
            )
        )

    def test_form_valid_remove_photo(self):
        photo = SimpleUploadedFile(
            name="test_image.jpg", content=b"content", content_type="image/jpeg"
        )
        self.user.photo = photo
        self.user.save()

        form_data = {
            "remove_photo": True,
            "username": self.username,
        }
        response = self.client.post(self.url, form_data, HTTP_REFERER=self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(username=self.username).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(message) == "Your profile has been updated." for message in messages
            )
        )
        self.user.refresh_from_db()
        self.assertFalse(bool(self.user.photo), "Photo should be deleted")
        self.assertEqual(self.user.photo, "", "Photo field should be empty")

    def test_form_invalid(self):
        form_data = {"email": self.invalid_email}
        response = self.client.post(self.url, form_data)
        self.assertIn("email", response.context["form"].errors)
        self.assertContains(response, "Failed to update your profile.")


class CustomPasswordChangeViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse("password_change")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/password_change/")
        self.assertEqual(
            view.func.__name__, CustomPasswordChangeView.as_view().__name__
        )

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "registration/password_change_form.html")
        self.assertIsInstance(self.response.context["form"], CustomPasswordChangeForm)

    def test_form_valid(self):
        form_data = {
            "old_password": self.password,
            "new_password1": "new_pass123",
            "new_password2": "new_pass123",
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                str(message) == "Password changed successfully." for message in messages
            )
        )

    def test_form_invalid(self):
        form_data = {
            "old_password": "wrong_password",
            "new_password1": "new_pass123",
            "new_password2": "new_pass123",
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "Password change failed.")


class CustomPasswordResetViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse("password_reset")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/password_reset/")
        self.assertEqual(view.func.__name__, CustomPasswordResetView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "registration/password_reset_form.html")
        self.assertIsInstance(self.response.context["form"], CustomPasswordResetForm)

    def test_form_valid(self):
        form_data = {"email": self.existing_email}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(
            str(messages[0]),
            "We've emailed you instructions for setting your password.",
        )

    def test_form_invalid(self):
        form_data = {"email": "nonexistentuser@mail.com"}
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)


class DeleteAccountViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse("delete_account")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/delete/")
        self.assertEqual(view.func.__name__, DeleteAccountView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "account/delete_account.html")
        self.assertIsInstance(self.response.context["form"], DeleteAccountForm)

    def test_successful_account_deletion(self):
        response = self.client.post(
            self.url, data={"password": self.password, "confirm_delete": True}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Profile.objects.filter(username=self.user).exists())

    def test_delete_with_incorrect_password(self):
        response = self.client.post(
            self.url, data={"password": "", "confirm_delete": True}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(username=self.user).exists())
        messages = list(response.context["messages"])
        self.assertEqual(
            str(messages[0]), "Incorrect password. Account deletion failed."
        )

    def test_delete_without_confirmation(self):
        response = self.client.post(
            self.url,
            data={
                "password": self.password,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.filter(username=self.user).exists())
        messages = list(response.context["messages"])
        self.assertEqual(
            str(messages[0]),
            "Please check the confirmation box to delete your account.",
        )
        self.assertFormError(
            response, "form", "confirm_delete", "This field is required."
        )


class UserCommentsViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.comment = Comment.objects.create(
            news=self.news, author=self.user, text="User comment"
        )
        self.url = reverse("user_comments")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/user_comments/")
        self.assertEqual(view.func.__name__, UserCommentsView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "account/user_comments.html")
        self.assertIn("user_comments", self.response.context)
        self.assertIn(self.comment, self.response.context["user_comments"])

    def test_view_pagination(self):
        for i in range(9):
            Comment.objects.create(news=self.news, author=self.user, text=f"Comment {i}")

        response = self.client.get(reverse("user_comments"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["user_comments"]), 8)

        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_comments']), 2)


class UserFavoriteStarsViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

        for i in range(9):
            name = f"Star {i + 1}"
            slug = slugify(name)
            star = Star.objects.create(name=name, slug=slug, spectrum=self.spectrum)
            FavoriteStar.objects.create(user=self.user, star=star)
        
        self.url = reverse("user_favorites")
        self.response = self.client.get(self.url)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/user_favorites/")
        self.assertEqual(view.func.__name__, UserFavoriteStarsView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, 'account/user_favorites.html')
        self.assertIn('user_favorites', self.response.context)
        self.assertEqual(len(self.response.context['user_favorites']), 8)

    def test_view_pagination(self):
        response = self.client.get(reverse('user_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['user_favorites']), 8)

        response = self.client.get(self.url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_favorites']), 1)


class UserWishListViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse("user_wish_list")
        self.response = self.client.get(self.url)
        self.wishlist = WishList.objects.get(user=self.user)
        self.wishlist.products.add(self.product1, self.product2)

    def test_page_status_and_view_url(self):
        self.assertEqual(self.response.status_code, 200)
        view = resolve("/account/wish_list/")
        self.assertEqual(view.func.__name__, UserWishListView.as_view().__name__)

    def test_correct_template_and_view_context(self):
        self.assertTemplateUsed(self.response, "account/user_wish_list.html")
        self.assertIn("cart_product_form", self.response.context)
        self.assertIsInstance(
            self.response.context["cart_product_form"], CartAddProductForm
        )

    def test_wishlist_creation_on_get(self):
        wishlist = WishList.objects.filter(user=self.user).first()
        self.assertIsNotNone(wishlist)
        self.assertEqual(wishlist.user, self.user)

    def test_post_adds_products_to_cart_and_deletes_wishlist(self):
        form_data = {
            'quantity': 1,
            'override': False,
            'delete_wishlist': True
        }
        response = self.client.post(self.url, data=form_data)
        self.assertRedirects(response, reverse('cart_detail'))

        cart = self.client.session.get('cart')
        self.assertIsNotNone(cart)
        self.assertIn(str(self.product1.id), cart)
        self.assertIn(str(self.product2.id), cart)
        self.assertEqual(WishList.objects.filter(user=self.user).count(), 0)

    def test_get_queryset_returns_correct_wishlist(self):
        view = UserWishListView()
        view.request = self.client.get(self.url).wsgi_request
        queryset = view.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.wishlist)

    def test_post_with_invalid_form(self):
        data = {
            'quantity': -1,
            'delete_wishlist': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user_wish_list.html')
        self.assertIn('form_errors', response.context)

        form_errors = response.context['form_errors']
        self.assertIn('quantity', form_errors)
        self.assertIn('Ensure this value is greater than or equal to 1.', form_errors['quantity'])
        self.assertFalse(self.client.session.get('cart', None))
