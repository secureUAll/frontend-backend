from django.urls import path
from .views import kafka_test, MachinesView

app_name = 'machines'

urlpatterns = [
    path('', MachinesView, name='machines'),
    path('kafka', kafka_test, name='kafka_test')
]
