from django.urls import path
from shop.views import ProductListView, ProductDetailView, WishListUpdateView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='products_by_category'),
    path('brand/<slug:brand_slug>/', ProductListView.as_view(), name='products_by_brand'),
    path('<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:product_slug>/wishlist/', WishListUpdateView.as_view(), name='wishlist'),
]
