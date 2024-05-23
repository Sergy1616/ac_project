from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView

from account.models import Profile


class LoginProfileView(LoginView):
    template_name = "registration/login.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "account/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
