from django.urls import path

from .views import WorkersView, AddMachinesView

app_name = 'workers'

urlpatterns = [
    path('', WorkersView.as_view(), name='workers'),
    path('<int:id>/machines/add', AddMachinesView.as_view(), name='addMachines'),
    path('<int:id>/machines/edit', AddMachinesView.as_view(edit=True), name='editMachines'),

]
