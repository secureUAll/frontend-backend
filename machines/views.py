from django.shortcuts import render

import machines.dataContext as dataContext

# Importing data context.
context = dataContext.machineContext

# Create your views here.
def MachinesView(request, *args, **kwargs):
    return render(request, "machines/machines.html", context)

def RequestsView(request, *args, **kwargs):
    return render(request, "machines/requests.html", context)