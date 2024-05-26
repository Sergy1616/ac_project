from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .utils import NavigationMixin
from .models import SpaceNews


class SpaceNewsView(ListView):
    model = SpaceNews
    template_name = "space/news.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return SpaceNews.objects.filter(published=True)


class SpaceNewsDetailView(NavigationMixin, DetailView):
    model = SpaceNews
    template_name = "space/news_detail.html"
    context_object_name = "news"
    slug_url_kwarg = "news_slug"
    navigate_on_field = "time_create"
    extra_filters = {"published": True}
    sort_order = "desc"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        news = get_object_or_404(SpaceNews, slug=slug, published=True)
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_list"] = reverse("news")
        return context
