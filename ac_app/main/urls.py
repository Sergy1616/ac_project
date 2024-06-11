from django.urls import path
from main.views import HomePageView, SearchView


urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('', HomePageView.as_view(), name='home'),
]
