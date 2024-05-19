from django.urls import path
from main.views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
