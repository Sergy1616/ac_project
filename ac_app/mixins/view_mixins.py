from django.db.models import Prefetch

from shop.models import Product, ProductImage


class OnSaleProductsMixin:
    def get_is_on_sale_products(self):
        return Product.objects.filter(in_stock=True, discount__gt=0).prefetch_related(
            Prefetch('images', queryset=ProductImage.objects.filter(is_for_slider=True))
        )
