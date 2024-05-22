from django.contrib.auth.views import LoginView


class LoginProfileView(LoginView):
    template_name = 'registration/login.html'
