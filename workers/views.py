from django.shortcuts import render

# Create your views here.
def WorkersView(request, *args, **kwargs):
    return render(request, "workers/workers.html", {})