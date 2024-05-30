from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.templatetags.static import static
from django.views.generic import ListView, DetailView

from .forms import ProductSortForm
from .models import Category, Product, Brand, ProductImage, WishList


class ProductListView(ListView):
    model = Product
    form_class = ProductSortForm
    template_name = 'shop/products.html'
    context_object_name = 'product_list'
    category_slug_url_kwarg = 'category_slug'
    brand_slug_url_kwarg = 'brand_slug'
    allow_empty = False
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
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
        queryset = self.get_sorted_queryset(queryset)

        return queryset

    def filter_by_category_and_brand(self, queryset):
        category_slug = self.kwargs.get(self.category_slug_url_kwarg)
        brand_slug = self.kwargs.get(self.brand_slug_url_kwarg)

        if category_slug:
            return queryset.filter(category__slug=category_slug)
        if brand_slug:
            return queryset.filter(brand__slug=brand_slug)

        return queryset

    def get_sorted_queryset(self, queryset):
        form = self.form_class(self.request.GET)
        if form.is_valid() and form.cleaned_data.get('sort'):
            sort_option = form.cleaned_data['sort']
            if sort_option == 'date_desc':
                queryset = queryset.order_by('-time_create')
            elif sort_option == 'price_desc':
                queryset = queryset.order_by('-price')
            elif sort_option == 'price_asc':
                queryset = queryset.order_by('price')
            elif sort_option == 'name_asc':
                queryset = queryset.order_by('name')
            elif sort_option == 'name_desc':
                queryset = queryset.order_by('-name')

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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProductImage.objects.filter(product=self.object, is_for_slider=False)

        if self.request.user.is_authenticated:
            context['in_wishlist'] = WishList.objects.filter(user=self.request.user, products=self.object).exists()
        else:
            context['in_wishlist'] = False
        return context


class WishListUpdateView(View):
    def post(self, request, product_slug):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'You must be logged in to add an item to your wishlist',
                'status': 'login_required'}, status=401)

        product = get_object_or_404(Product, slug=product_slug)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            return JsonResponse({
                'result': 'removed',
                'action': 'Add to Wish List',
                'image_src': static('images/favourite_a.svg')
            })
        else:
            wishlist.products.add(product)
            return JsonResponse({
                'result': 'added',
                'action': 'Remove from Wish List',
                'image_src': static('images/favourite_r.svg')
            })
