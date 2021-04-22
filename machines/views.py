from django.shortcuts import render

# Create your views here.
def MachinesView(request, *args, **kwargs):
    return render(request, "machines/machines.html", {}
    )