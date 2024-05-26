from django.urls import path

from .views import SpaceNewsView


urlpatterns = [
    path('news/', SpaceNewsView.as_view(), name='news'),
]
