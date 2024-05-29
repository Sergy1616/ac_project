from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginProfileView,
    ProfileView,
    SignUpProfileView,
    EditProfileView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    DeleteAccountView,
    UserCommentsView,
    UserFavoriteStarsView
)

urlpatterns = [
    path('login/', LoginProfileView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpProfileView.as_view(), name='signup'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),

    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('user_comments/', UserCommentsView.as_view(), name='user_comments'),
    path('user_favorites/', UserFavoriteStarsView.as_view(), name='user_favorites'),
    path('<username>/', ProfileView.as_view(), name='user_detail'),
]
