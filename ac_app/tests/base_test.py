from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from shop.models import Category, Brand, Product, WishList
from space.models import SpectralClass, SpaceNews, Constellation

Profile = get_user_model()


class BaseTest(TestCase):

    def setUp(self):
        # account
        self.existing_user = "existinguser"
        self.existing_email = "existinguser@mail.com"
        self.password = "testpass123"

        self.username = "testuser"
        self.email = "testuser@mail.com"
        self.invalid_email = "invalid_email.com"

        self.user = self.create_user(
            username=self.existing_user,
            email=self.existing_email,
            password=self.password,
        )

        # space
        self.news = SpaceNews.objects.create(
            title="Test News", slug="test-news", description="News Description"
        )
        self.constellation = Constellation.objects.create(
            name="Test Constellation", slug="test-constellation"
        )
        self.spectrum = SpectralClass.objects.create(
            name="Test Spectral",
            slug="test-spectral",
            color="Test color",
            temperature="Test temperature",
            features="Test features",
        )

        # shop
        self.category = Category.objects.create(
            name="Test Category", slug="test-category"
        )
        self.brand = Brand.objects.create(
            name="Test Brand", slug="test-brand", image="test_image.png"
        )
        self.product1 = self.create_product(
            name="Test Product 1", slug="test-product-1"
        )
        self.product2 = self.create_product(
            name="Test Product 2", slug="test-product-2", price=200.00
        )
        self.wishlist = WishList.objects.create(user=self.user)

    def get_test_form_data(self, **kwargs):
        default_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }
        default_data.update(kwargs)
        return default_data

    def get_test_product_data(self, **kwargs):
        default_data = {
            "category": self.category,
            "name": "Test Product",
            "slug": "test-product",
            "brand": self.brand,
            "price": 100.00,
            "discount": 0,
        }
        default_data.update(kwargs)
        return default_data

    def create_user(self, **kwargs):
        default_data = {"username": self.username, "password": self.password}
        default_data.update(kwargs)
        return Profile.objects.create_user(**default_data)

    def create_product(self, **kwargs):
        product_data = self.get_test_product_data(**kwargs)
        return Product.objects.create(**product_data)
