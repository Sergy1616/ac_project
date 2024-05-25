from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
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


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'class': 'edit-input'}))
    remove_photo = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))

    class Meta:
        model = Profile
        fields = ['photo', 'remove_photo', 'username', 'first_name', 'last_name', 'email', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'edit-input'}),
            'last_name': forms.TextInput(attrs={'class': 'edit-input'}),
            'email': forms.EmailInput(attrs={'class': 'edit-input'}),
            'photo': forms.FileInput(attrs={'class': 'edit-img-input'}),
            'bio': forms.Textarea(attrs={'class': 'edit-text-input'}),
        }

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = Profile.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return data


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.user.has_usable_password():
            self.fields.pop('old_password')
        self.fields['new_password2'].label = 'Confirm password'

    class Meta:
        model = Profile
        fields = ['old_password', 'new_password1', 'new_password2']


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = Profile
        fields = ['email']

    def clean_email(self):
        data = self.cleaned_data['email'].lower()
        if not Profile.objects.filter(email=data).exists():
            raise forms.ValidationError('No account found with that email address.')
        return data


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_delete = forms.BooleanField(label='I understand that this action is irreversible')
