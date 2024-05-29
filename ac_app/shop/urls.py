from django.urls import path
from shop.views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='products_by_category'),
    path('brand/<slug:brand_slug>/', ProductListView.as_view(), name='products_by_brand'),
]
