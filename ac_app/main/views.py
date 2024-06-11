from django.views.generic import FormView, ListView, TemplateView
from itertools import chain
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
    TrigramSimilarity,
)

from .forms import SearchForm
from space.models import Star, SpaceNews, Constellation
from shop.models import Product


class HomePageView(TemplateView):
    template_name = "main/home.html"


class SearchView(FormView, ListView):
    form_class = SearchForm
    context_object_name = "results"
    success_url = "/search/"
    template_name = "main/search.html"
    paginate_by = 8

    def annotate_queryset(self, model, query, field_name, prefetch_related=None):
        queryset = []
        search_query = SearchQuery(query, config="english")
        if model == SpaceNews:
            vector = SearchVector("title", weight="A") + SearchVector(
                "description", weight="B"
            )
        else:
            vector = SearchVector("name", weight="A") + SearchVector(
                "description", weight="B"
            )

        queryset = (
            model.objects.annotate(
                rank=SearchRank(vector, search_query),
                similarity=TrigramSimilarity(field_name, query),
                headline=SearchHeadline(
                    field_name,
                    search_query,
                    config="english",
                    start_sel="<span>",
                    stop_sel="</span>",
                ),
                headline_description=SearchHeadline(
                    "description",
                    search_query,
                    config="english",
                    start_sel="<span>",
                    stop_sel="</span>",
                ),
            )
            .filter(rank__gte=0.3)
            .order_by("-rank")
        )
        if prefetch_related:
            queryset = queryset.prefetch_related(prefetch_related)

        return queryset

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            if query:
                news = self.annotate_queryset(SpaceNews, query, "title")
                constellations = self.annotate_queryset(Constellation, query, "name")
                stars = self.annotate_queryset(Star, query, "name")
                products = self.annotate_queryset(
                    Product, query, "name", prefetch_related="images"
                )

                queryset = list(chain(news, constellations, stars, products))
                self.total_results = len(queryset)
            else:
                self.total_results = 0
                queryset = []
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query")
        context["total_results"] = self.total_results
        return context
