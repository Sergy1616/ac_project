from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import SpaceNews


class SpaceNewsView(ListView):
    model = SpaceNews
    template_name = "space/news.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return SpaceNews.objects.filter(published=True)


class SpaceNewsDetailView(DetailView):
    model = SpaceNews
    template_name = "space/news_detail.html"
    context_object_name = "news"
    slug_url_kwarg = "news_slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        news = get_object_or_404(SpaceNews, slug=slug, published=True)
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        next_news = (
            SpaceNews.objects.filter(
                published=True, time_create__gt=self.object.time_create
            )
            .order_by("time_create")
            .first()
        )
        prev_news = (
            SpaceNews.objects.filter(
                published=True, time_create__lt=self.object.time_create
            )
            .order_by("-time_create")
            .first()
        )

        context["prev_news"] = prev_news
        context["next_news"] = next_news
        context["news_list"] = reverse("news")
        return context
