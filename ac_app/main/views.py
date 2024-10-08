from django.shortcuts import get_object_or_404
from django.views.generic import FormView, ListView, TemplateView
from itertools import chain
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
    TrigramSimilarity,
)

from mixins.view_mixins import OnSaleProductsMixin
from space.models import Star, SpaceNews, Constellation, StarCharacteristics
from shop.models import Product


class HomePageView(OnSaleProductsMixin, TemplateView):
    template_name = "main/home.html"
    LATEST_NEWS_COUNT = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slider_star"] = get_object_or_404(Star.objects.only("slug"), slug="sun")
        context["latest_news"] = self.get_latest_news()
        context["sale_products"] = self.get_is_on_sale_products()
        context["oldest_stars"] = self.get_list_of_oldest_stars()
        context["massive_stars"] = self.get_list_of_most_massive_stars()
        return context

    def get_latest_news(self):
        return SpaceNews.objects.filter(published=True).order_by("-time_create")[
            : self.LATEST_NEWS_COUNT
        ]

    def get_list_of_oldest_stars(self):
        oldest_stars = (
            StarCharacteristics.objects.filter(age_unit=2)
            .order_by("-age")
            .select_related("star")
            .only("age", "age_unit", "star__name", "star__image", "star__slug")
        )
        return oldest_stars

    def get_list_of_most_massive_stars(self):
        most_massive_stars = (
            StarCharacteristics.objects.filter(mass__gt=10)
            .order_by("-mass")
            .select_related("star")
            .only("mass", "star__name", "star__image", "star__slug")
        )
        return most_massive_stars


class SearchView(ListView):
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
        query = self.request.GET.get("query", "").strip()

        if not query:
            self.total_results = 0
            return []

        news = self.annotate_queryset(SpaceNews, query, "title")
        constellations = self.annotate_queryset(Constellation, query, "name")
        stars = self.annotate_queryset(Star, query, "name")
        products = self.annotate_queryset(
            Product, query, "name", prefetch_related="images"
        )

        queryset = sorted(
            chain(news, constellations, stars, products),
            key=lambda item: item.rank or 0,
            reverse=True,
        )

        self.total_results = len(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query")
        context["total_results"] = self.total_results
        return context
