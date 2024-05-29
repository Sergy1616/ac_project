from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Category, Product, Brand, ProductImage


class ProductListView(ListView):
    model = Product
    template_name = "shop/products.html"
    context_object_name = "product_list"
    category_slug_url_kwarg = 'category_slug'
    brand_slug_url_kwarg = 'brand_slug'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context.update(self.get_selected_context())
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(in_stock=True)
        queryset = self.filter_by_category_and_brand(queryset)
        queryset = queryset.select_related('category', 'brand').prefetch_related(
            'images',
            Prefetch('images', queryset=ProductImage.objects.filter(title_image=True),
                     to_attr='title_images')
        )
        return queryset

    def filter_by_category_and_brand(self, queryset):
        category_slug = self.kwargs.get(self.category_slug_url_kwarg)
        brand_slug = self.kwargs.get(self.brand_slug_url_kwarg)

        if category_slug:
            return queryset.filter(category__slug=category_slug)
        if brand_slug:
            return queryset.filter(brand__slug=brand_slug)

        return queryset

    def get_selected_context(self):
        category_slug = self.kwargs.get(self.category_slug_url_kwarg)
        brand_slug = self.kwargs.get(self.brand_slug_url_kwarg)
        context = {}

        if category_slug:
            context['selected_category'] = get_object_or_404(Category, slug=category_slug)
        if brand_slug:
            context['selected_brand'] = get_object_or_404(Brand, slug=brand_slug)

        return context
