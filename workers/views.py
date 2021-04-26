from django.shortcuts import render
from django.views import View

import workers.dataContext as dataContext

# Create your views here.
class WorkersView(View):

    def get(self, request, *args, **kwargs):
        context = dataContext.workersContext
        return render(request, "workers/workers.html", context)

class NewWorkerView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "workers/newWorker.html", )
