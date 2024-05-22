from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from account.htmx_views import check_username_or_email_htmx, check_password_htmx, login_user_htmx


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),

    path('', include('main.urls')),
]

htmx_urlpatterns = [
    path('check_user/', check_username_or_email_htmx, name='check-user'),
    path('check_password/', check_password_htmx, name='check-password'),
    path('login_user/', login_user_htmx, name='login_user')
]

urlpatterns += htmx_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
