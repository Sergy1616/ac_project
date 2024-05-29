from django.templatetags.static import static
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from .utils import NavigationMixin, PaginatedListView
from .models import (
    SpaceNews,
    Comment,
    Constellation,
    SpectralClass,
    Star,
    StarCharacteristics,
    FavoriteStar
)
from .forms import CommentForm


class SpaceNewsView(PaginatedListView):
    model = SpaceNews
    template_name = "space/news.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return SpaceNews.objects.filter(published=True)

    def get_ajax_template_name(self):
        return "include/space/other_news.html"


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
        news = get_object_or_404(SpaceNews.objects.prefetch_related(
            "comments__author"), slug=slug, published=True)
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_list"] = reverse("news")
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.filter(active=True)
        return context


class CommentView(LoginRequiredMixin, View):
    def post(self, request, slug):
        news = get_object_or_404(SpaceNews, slug=slug)
        form = CommentForm(request.POST)
        comment_id = request.POST.get("comment_id")
        if form.is_valid():
            if comment_id:
                comment = get_object_or_404(Comment, pk=comment_id, author=request.user, news=news)
                comment.text = form.cleaned_data["text"]
            else:
                comment = form.save(commit=False)
                comment.author = request.user
                comment.news = news
            comment.save()
        return redirect(news.get_absolute_url())


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        news = get_object_or_404(SpaceNews, slug=slug)
        comment_id = request.POST.get("comment_id")
        comment = get_object_or_404(Comment, pk=comment_id, author=request.user, news=news)
        comment.delete()
        referer_url = request.META.get("HTTP_REFERER")
        return HttpResponseRedirect(referer_url)


class ConstellationView(PaginatedListView):
    model = Constellation
    template_name = "space/constellations.html"
    context_object_name = "constellation_list"

    def get_ajax_template_name(self):
        return "include/space/other_constellations.html"


class ConstellationDetailView(NavigationMixin, DetailView):
    model = Constellation
    template_name = "space/constellation_detail.html"
    context_object_name = "constellation"
    navigate_on_field = "name"
    sort_order = "asc"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["constellation_list"] = reverse("constellations")
        context["stars"] = Star.objects.filter(constellation=self.object)
        return context


class StarsView(PaginatedListView):
    model = Star
    template_name = "space/stars.html"
    context_object_name = "stars_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classes"] = SpectralClass.objects.all()
        return context

    def get_queryset(self):
        if hasattr(self, "_filtered_queryset"):
            return self._filtered_queryset

        queryset = Star.objects.select_related("spectrum").prefetch_related("constellation")
        spectral_slug = self.request.GET.get("spectral")
        if spectral_slug:
            spectral_class = get_object_or_404(SpectralClass, slug=spectral_slug)
            queryset = queryset.filter(spectrum__slug=spectral_slug)

        # ! for "select_related" method (SpectralClass similar queries)
        self._filtered_queryset = queryset
        return queryset

    def get_ajax_template_name(self):
        return "include/space/other_stars.html"


class StarsDetailView(NavigationMixin, DetailView):
    model = Star
    template_name = "space/star_detail.html"
    context_object_name = "star"
    navigate_on_field = "name"
    sort_order = "asc"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["characteristics"] = StarCharacteristics.objects.filter(star=self.object)
        context["stars_list"] = reverse("stars")

        star = self.object  # ! similar queries
        if self.request.user.is_authenticated:
            context["is_favorite"] = FavoriteStar.objects.filter(user=self.request.user, star=star).exists()
        else:
            context["is_favorite"] = False

        return context


class FavoriteStarView(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            return JsonResponse({
                "error": "You must be logged in to add stars to favorites",
                "status": "login_required"}, status=401)

        star = get_object_or_404(Star, slug=slug)

        favorite, created = FavoriteStar.objects.get_or_create(user=request.user, star=star)
        if not created:
            favorite.delete()
            return JsonResponse({
                "result": "removed",
                "action": "Add to Favorites",
                "image_src": static("images/favourite_a.svg")
            })
        else:
            return JsonResponse({
                "result": "added",
                "action": "Remove from Favorites",
                "image_src": static("images/favourite_r.svg")
            })
