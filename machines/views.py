from django.shortcuts import render

import machines.dataContext as dataContext

# Create your views here.
def MachinesView(request, *args, **kwargs):
    context = dataContext.machineContext
    return render(request, "machines/machines.html", context)