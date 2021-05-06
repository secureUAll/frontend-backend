from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import workers.dataContext as dataContext

from .models import Worker

# Create your views here.


class WorkersView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {'workers': Worker.objects.all().order_by('-created')}
        return render(request, "workers/workers.html", context)


class NewWorkerView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'machines': [m for worker in dataContext.workersContext['workers'] for m in worker['machinesList']]
        }
        return render(request, "workers/newWorker.html", context)
