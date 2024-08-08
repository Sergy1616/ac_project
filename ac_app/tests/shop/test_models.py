from django.core.exceptions import ValidationError
from django.urls import reverse, NoReverseMatch

from tests.base_test import BaseTest
from shop.models import Category, ProductImage, WishList


class CategoryModelTest(BaseTest):
    def test_create_category(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.slug, "test-category")

    def test_str_method(self):
        self.assertEqual(str(self.category), "Test Category")

    def test_category_absolute_url(self):
        category = Category.objects.get(name="Test Category")
        self.assertEqual(
            category.get_absolute_url(),
            reverse("products_by_category", kwargs={"category_slug": "test-category"}),
        )


class BrandModelTest(BaseTest):
    def test_create_brand(self):
        self.assertEqual(self.brand.name, "Test Brand")
        self.assertEqual(self.brand.slug, "test-brand")
        self.assertEqual(self.brand.image, "test_image.png")
        expected_upload_path = f"brands/{self.brand.slug}/test_image.png"
        self.assertEqual(self.brand.upload_img("test_image.png"), expected_upload_path)

    def test_str_method(self):
        self.assertEqual(str(self.brand), "Test Brand")

    def test_brand_get_absolute_url(self):
        self.assertEqual(
                self.brand.get_absolute_url(),
                reverse("products_by_brand", kwargs={"brand_slug": self.brand.slug}),
            )


class ProductModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.product = self.create_product(price=999999.99, discount=10)

    def test_create_product(self):
        self.assertEqual(str(self.product.category), "Test Category")
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.slug, "test-product")
        self.assertEqual(str(self.product.brand), "Test Brand")
        self.assertEqual(self.product.price, 999999.99)
        self.assertEqual(self.product.discount, 10)

    def test_str_method(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_product_get_absolute_url(self):
        try:
            self.assertEqual(
                self.product.get_absolute_url(),
                reverse("product_detail", kwargs={"product_slug": self.product.slug}),
            )
        except NoReverseMatch:
            self.fail(
                "Reversed URL 'product_detail' with kwargs={'product_slug': self.product.slug} not found."
            )

    def test_final_price_with_discount(self):
        self.assertEqual(self.product.final_price(), 899999.99)

    def test_final_price_without_discount(self):
        product_no_discount = self.create_product(
            name="Test Product No Discount",
            slug="test-product-no-discount"
        )
        self.assertEqual(product_no_discount.final_price(), 100.00)

    def test_product_without_brand(self):
        product_without_brand = self.create_product(
            name="Test Product Without Brand",
            slug="test-product-without-brand",
            brand=None
        )
        self.assertIsNone(product_without_brand.brand)

    def test_product_discount_out_of_bounds(self):
        product_high_discount = self.create_product(
            name="Test Product High Discount",
            slug="test-product-high-discount",
            discount=105
        )
        with self.assertRaises(ValidationError):
            product_high_discount.full_clean()

        product_negative_discount = self.create_product(
            name="Test Product Negative Discount",
            slug="test-product-negative-discount",
            discount=-5
        )
        with self.assertRaises(ValidationError):
            product_negative_discount.full_clean()

    def test_product_default_in_stock(self):
        self.assertTrue(self.product.in_stock)

    def test_product_time_create(self):
        self.assertIsNotNone(self.product.time_create)

    def test_product_time_updated(self):
        self.assertIsNotNone(self.product.time_updated)


class ProductImageModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.product = self.create_product()
        self.product_image = ProductImage.objects.create(
            product=self.product,
            image="test_image.jpg",
            title_image=True,
            is_for_slider=True,
        )

    def test_create_image(self):
        self.assertEqual(self.product_image.product, self.product)
        self.assertEqual(self.product_image.image, "test_image.jpg")

        expected_upload = (
            f"product_images/{self.product_image.product.category.slug}"
            f"/{self.product_image.product.slug}/test_image.jpg"
        )
        self.assertEqual(
            self.product_image.upload_img("test_image.jpg"), expected_upload
        )

    def test_product_image_title_image(self):
        product_image = ProductImage.objects.get(image="test_image.jpg")
        self.assertTrue(product_image.title_image)

    def test_product_image_is_for_slider(self):
        product_image = ProductImage.objects.get(image="test_image.jpg")
        self.assertTrue(product_image.is_for_slider)


class WishListModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.wishlist = WishList.objects.create(user=self.user)

    def test_create_wishlist(self):
        self.assertEqual(self.wishlist.user, self.user)
        self.assertEqual(self.wishlist.title, "Wish List")
        self.assertEqual(self.wishlist.products.count(), 0)

    def test_str_method(self):
        self.assertEqual(str(self.wishlist), f"Wish List - {self.user}")

    def test_add_products_to_wishlist(self):
        self.wishlist.products.add(self.product1, self.product2)
        self.assertEqual(self.wishlist.products.count(), 2)
        self.assertIn(self.product1, self.wishlist.products.all())
        self.assertIn(self.product2, self.wishlist.products.all())

    def test_remove_products_from_wishlist(self):
        self.wishlist.products.add(self.product1, self.product2)
        self.wishlist.products.remove(self.product1)
        self.assertEqual(self.wishlist.products.count(), 1)
        self.assertIn(self.product2, self.wishlist.products.all())
        self.assertNotIn(self.product1, self.wishlist.products.all())
