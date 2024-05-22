from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginProfileView


urlpatterns = [
    path('login/', LoginProfileView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
