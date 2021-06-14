from django.urls import path
from .views import LoginView, LogoutView, WelcomeView, ProfileView

app_name = 'login'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('profile/', ProfileView.as_view(), name='profile'),
]