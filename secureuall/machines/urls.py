from django.urls import path
from .views import kafka_test

app_name = 'machines'

urlpatterns = [
    path('kafka', kafka_test, name='kafka_test')
]
