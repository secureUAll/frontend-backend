from django.urls import path

from .views import DashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView, name='dashboard')
]