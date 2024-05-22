from django.contrib.auth.views import LoginView
from .forms import SignInProfileForm


class LoginProfileView(LoginView):
    form_class = SignInProfileForm
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = context.pop('form')
        return context
