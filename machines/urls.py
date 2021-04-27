from django.urls import path

from .views import MachinesView
from .views import RequestsView

app_name = 'machines'

urlpatterns = [
    path('', MachinesView, name='machines'),
    path('requests', RequestsView, name='requests'),
]