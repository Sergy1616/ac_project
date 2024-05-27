from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .utils import NavigationMixin
from .models import SpaceNews, Comment
from .forms import CommentForm


class SpaceNewsView(ListView):
    model = SpaceNews
    template_name = "space/news.html"
    context_object_name = "news_list"
    paginate_by = 4

    def get_queryset(self):
        return SpaceNews.objects.filter(published=True)

    # pagination
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        news_object_list = request.GET.get("news_object_list")

        if news_object_list:
            page = request.GET.get("page")
            paginator = Paginator(self.object_list, self.paginate_by)
            try:
                news_list = paginator.page(page)
            except PageNotAnInteger:
                news_list = paginator.page(1)
            except EmptyPage:
                return HttpResponse("")

            context = {"news_list": news_list}
            return render(request, "include/space/other_news.html", context)

        else:
            context = self.get_context_data()
            return self.render_to_response(context)


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
