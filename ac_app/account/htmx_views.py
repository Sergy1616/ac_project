from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods


def get_user_by_username_or_email(username_or_email):
    User = get_user_model()
    if "@" in username_or_email:
        return User.objects.filter(email=username_or_email).first()
    return User.objects.filter(username=username_or_email).first()


@require_http_methods(["POST"])
def check_username_or_email_htmx(request):
    username_or_email = request.POST.get("username_or_email", "").strip().lower()
    user = get_user_by_username_or_email(username_or_email)
    if not user:
        return HttpResponse(f'No user with this {"email" if "@" in username_or_email else "username"} exists')
    return HttpResponse('<div class="login-success"></div>') # для отображения '🗸' в css

@require_http_methods(["POST"])
def check_password_htmx(request):
    username_or_email = request.POST.get("username_or_email", "").strip().lower()
    password = request.POST.get("password")
    user = get_user_by_username_or_email(username_or_email)

    if not user:
        return HttpResponse("No user with this username or email exists")

    if len(password) < 8:
        return HttpResponse("Your password must be at least 8 characters long")

    if not check_password(password, user.password):
        return HttpResponse("Incorrect password")

    return HttpResponse('<div class="password-success"></div>')

@require_http_methods(["POST"])
def login_user_htmx(request):
    username_or_email = request.POST.get("username_or_email", "").lower().strip()
    password = request.POST.get("password", "").strip()
    user = authenticate(request, username=username_or_email, password=password)

    if user is None:
        return HttpResponse("Invalid username or password", status=401, headers={'HX-Redirect': '/account/login/'})

    login(request, user)
    return JsonResponse({'message': f'Welcome {user.username}!'}, headers={'HX-Trigger': 'loginSuccess'})
