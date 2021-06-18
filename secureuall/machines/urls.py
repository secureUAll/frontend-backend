from django.urls import path

from login.views import WelcomeView
from .views import kafka_test, MachinesView, RequestsView, LogView

app_name = 'machines'

urlpatterns = [
    path('<int:id>', MachinesView, name='machines'),
    path('requests', RequestsView.as_view(), name='requests'),
    path('requests/new', WelcomeView.as_view(incoming=False, template_name="machines/requests_new.html"), name='requests_new'),
    path('logs/<int:id>', LogView.as_view(), name='getLog'),
    path('kafka', kafka_test, name='kafka_test')
]
