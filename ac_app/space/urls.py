from django.urls import path

from .views import SpaceNewsView, SpaceNewsDetailView


urlpatterns = [
    path('news/', SpaceNewsView.as_view(), name='news'),
    path('news/<slug:news_slug>/', SpaceNewsDetailView.as_view(), name='news_detail'),
]
