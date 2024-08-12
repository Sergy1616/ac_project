from shop.admin import ProductAdmin, WishListAdmin
from shop.models import Product, WishList
from tests.base_test import BaseTest


class ProductAdminTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.admin = ProductAdmin(model=Product, admin_site=None)

    def test_final_price_display(self):
        expected_final_price = self.product1.final_price()
        final_price_display = self.admin.final_price_display(self.product1)
        self.assertEqual(final_price_display, expected_final_price)


class WishListAdminTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.wishlist.products.add(self.product1, self.product2)
        self.admin = WishListAdmin(model=WishList, admin_site=None)

    def test_get_product_count(self):
        product_count = self.admin.get_product_count(self.wishlist)
        self.assertEqual(product_count, 2)
