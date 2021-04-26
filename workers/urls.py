from django.urls import path

from .views import WorkersView

app_name = 'workers'

urlpatterns = [
    path('', WorkersView.as_view(), name='workers')
]