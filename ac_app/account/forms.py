from django.contrib.auth.forms import AuthenticationForm



class SignInProfileForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()
