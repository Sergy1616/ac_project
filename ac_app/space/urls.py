from django.urls import path

from .views import (
    SpaceNewsView,
    SpaceNewsDetailView,
    CommentView,
    CommentDeleteView,
    ConstellationView,
    ConstellationDetailView,
    StarsView,
    StarsDetailView,
    FavoriteStarView
)

urlpatterns = [
    path('news/', SpaceNewsView.as_view(), name='news'),
    path('news/<slug:news_slug>/', SpaceNewsDetailView.as_view(), name='news_detail'),
    path('news/<slug:slug>/comment/', CommentView.as_view(), name='comment_view'),
    path('news/<slug:slug>/comment_delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('constellations/', ConstellationView.as_view(), name='constellations'),
    path('constellations/<slug:slug>/', ConstellationDetailView.as_view(), name='constellation_detail'),
    path('stars/', StarsView.as_view(), name='stars'),
    path('stars/<slug:slug>/', StarsDetailView.as_view(), name='star_detail'),
    path('stars/<slug:slug>/favorite/', FavoriteStarView.as_view(), name='favorite'),
]
