from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

Profile = get_user_model()


class SignInProfileForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.lower()


class SignUpProfileForm(UserCreationForm):
    username = forms.CharField(min_length=5)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if Profile.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
