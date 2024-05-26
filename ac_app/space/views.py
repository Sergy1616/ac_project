from django.views.generic import ListView
from .models import SpaceNews


class SpaceNewsView(ListView):
    model = SpaceNews
    template_name = 'space/news.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return SpaceNews.objects.filter(published=True)
