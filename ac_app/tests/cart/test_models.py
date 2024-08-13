from decimal import Decimal
from django.test import RequestFactory

from app import settings
from cart.cart import Cart
from tests.base_test import BaseTest


class CartTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.session = self.client.session

    def create_cart(self):
        request = self.factory.get("/")
        request.session = self.session
        return Cart(request)

    def test_add_product_to_cart(self):
        cart = self.create_cart()
        cart.add(self.product1.id)
        cart.save()
        self.assertIn(str(self.product1.id), cart.session[settings.CART_SESSION_ID])

    def test_update_product_quantity_in_cart(self):
        cart = self.create_cart()
        cart.add(self.product1.id, quantity=5)
        cart.add(self.product1.id, quantity=3)
        self.session.save()
        self.assertEqual(cart.cart[str(self.product1.id)]["quantity"], 8)

    def test_override_product_quantity_in_cart(self):
        cart = self.create_cart()
        cart.add(self.product1.id, quantity=5)
        cart.add(self.product1.id, quantity=10, override_quantity=True)
        self.session.save()
        self.assertEqual(cart.cart[str(self.product1.id)]["quantity"], 10)

    def test_remove_product_from_cart(self):
        cart = self.create_cart()
        cart.add(self.product1.id)
        cart.remove(self.product1.id)
        self.session.save()
        self.assertNotIn(str(self.product1.id), cart.cart)

    def test_total_unique_items(self):
        cart = self.create_cart()
        cart.add(self.product1.id, quantity=3)
        cart.add(self.product2.id, quantity=2)
        self.session.save()
        self.assertEqual(cart.total_unique_items(), 2)

    def test_total_price(self):
        cart = self.create_cart()
        cart.add(self.product1.id, quantity=1)
        cart.add(self.product2.id, quantity=2)
        self.session.save()
        total_price = (
            Decimal(self.product1.final_price()) * 1
            + Decimal(self.product2.final_price()) * 2
        )
        self.assertEqual(cart.get_total_price(), total_price)

    def test_clear_cart(self):
        cart = self.create_cart()
        cart.add(self.product1.id)
        cart.clear()
        self.session.save()
        self.assertEqual(len(cart.session.get(settings.CART_SESSION_ID, {})), 0)
        cart = self.create_cart()
        self.assertEqual(len(cart), 0)
