from account.forms import SignInProfileForm


def login_form(request):
    return {'login_form': SignInProfileForm()}
