from django.urls import path
from .views import kafka_test, MachinesView, RequestsView

app_name = 'machines'

urlpatterns = [
    path('<int:id>', MachinesView, name='machines'),
    path('requests', RequestsView.as_view(), name='requests'),
    path('kafka', kafka_test, name='kafka_test')
]
