from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.shortcuts import redirect

from account.forms import CustomPasswordResetForm, SignUpProfileForm, ProfileEditForm, CustomPasswordChangeForm
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


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'account/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.cleaned_data['remove_photo']:
            self.object.photo.delete()
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been updated.")
        referer_url = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer_url) if referer_url else response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Failed to update your profile.")
        return response


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change')
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully.")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Password change failed.")
        return response


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            form.save(request=request)
            messages.success(request, "We've emailed you instructions for setting your password.")
            return self.get(request, *args, **kwargs)
        else:
            return self.form_invalid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been set successfully.")
            return self.get(request, *args, **kwargs)
        else:
            return self.form_invalid(form)
