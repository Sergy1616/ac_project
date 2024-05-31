from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.products_cache = None

    def add(self, product_id, quantity=1, override_quantity=False):
        """
        Добавление товара в корзину или обновление его количества
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
        Отметить сессию как "modified", чтобы убедиться, что она сохранится
        """
        self.session.modified = True
        self.products_cache = None

    def remove(self, product_id):
        """
        Удаление товара из корзины
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def total_unique_items(self):
        """
        Возвращает количество уникальных товаров в корзине
        """
        return len(self.cart)

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных
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
        Подсчет всех товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Расчет общей стоимости корзины, учитывая скидки на товары
        """
        return sum(Decimal(item['product'].final_price()) * item['quantity'] for item in self)

    def clear(self):
        """
        Удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
