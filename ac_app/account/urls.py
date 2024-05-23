from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginProfileView, ProfileView, SignUpProfileView


urlpatterns = [
    path('login/', LoginProfileView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpProfileView.as_view(), name='signup'),
    path('<username>/', ProfileView.as_view(), name='user_detail'),
]
