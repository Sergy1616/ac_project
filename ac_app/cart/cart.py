from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Initializes the cart. If the cart is not in the session, it creates a new empty cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.products_cache = None

    def add(self, product_id, quantity=1, override_quantity=False):
        """
        Adds a product to the cart or updates its quantity.
        If the override_quantity flag is set, it replaces the current quantity with the given quantity.
        Otherwise, it adds the given quantity to the existing quantity of the product.
        """
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(get_object_or_404(Product, id=product_id).price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Marks the session as modified to ensure it gets saved, and clears the product cache
        """
        self.session.modified = True
        self.products_cache = None

    def remove(self, product_id):
        """
        Removes a product from the cart
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def total_unique_items(self):
        """
        Returns the number of unique items in the cart
        """
        return len(self.cart)

    def __iter__(self):
        """
        Iterates over the items in the cart and attaches the actual product object to each item
        """
        product_ids = self.cart.keys()
        if self.products_cache is None:
            self.products_cache = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in self.products_cache:
            if str(product.id) in cart:
                item = cart[str(product.id)]
                item['product'] = product
                item['price'] = Decimal(product.final_price())
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """
        Returns the total number of items in the cart including all quantities
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculates and returns the total price of all items in the cart
        """
        return sum(Decimal(item['product'].final_price()) * item['quantity'] for item in self)

    def clear(self):
        """
        Clears the cart from the session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
