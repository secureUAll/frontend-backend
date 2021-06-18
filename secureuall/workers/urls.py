from django.urls import path

from .views import WorkersView, AddMachinesView, WorkerLogsView

app_name = 'workers'

urlpatterns = [
    path('', WorkersView.as_view(), name='workers'),
    path('<int:id>/machines/add/batch', AddMachinesView.as_view(mode="batch"), name='addMachines'),
    path('<int:id>/machines/add/range', AddMachinesView.as_view(mode="range"), name='addMachinesRange'),
    path('<int:id>/machines/edit', AddMachinesView.as_view(edit=True), name='addMachines'),
    path('<int:id>/logs/', WorkerLogsView.as_view(), name='workerLogs'),
]
