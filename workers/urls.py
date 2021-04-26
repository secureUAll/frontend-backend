from django.urls import path

from .views import WorkersView, NewWorkerView

app_name = 'workers'

urlpatterns = [
    path('', WorkersView.as_view(), name='workers'),
    path('new', NewWorkerView.as_view(), name='newworker'),
]
