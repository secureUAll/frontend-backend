from django.urls import path

from .views import MachinesView

app_name = 'machines'

urlpatterns = [
    path('', MachinesView, name='machines'),
]