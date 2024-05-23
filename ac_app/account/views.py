from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, FormView
from django.shortcuts import redirect

from account.forms import SignUpProfileForm
from account.models import Profile


class LoginProfileView(LoginView):
    template_name = "registration/login.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "account/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"


class SignUpProfileView(FormView):
    form_class = SignUpProfileForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_form'] = self.get_form()
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='account.authentication.EmailAuthBackend')
        return redirect('user_detail', username=user.username)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Failed to register your account.")
        return response
