from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import SpaceNews


class SpaceNewsView(ListView):
    model = SpaceNews
    template_name = 'space/news.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return SpaceNews.objects.filter(published=True)


class SpaceNewsDetailView(DetailView):
    model = SpaceNews
    template_name = 'space/news_detail.html'
    context_object_name = 'news'
    slug_url_kwarg = 'news_slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        news = get_object_or_404(SpaceNews, slug=slug, published=True)
        return news
