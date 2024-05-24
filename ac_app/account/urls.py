from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginProfileView, ProfileView, SignUpProfileView, EditProfileView


urlpatterns = [
    path('login/', LoginProfileView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpProfileView.as_view(), name='signup'),
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('<username>/', ProfileView.as_view(), name='user_detail'),
]
