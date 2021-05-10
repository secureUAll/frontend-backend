from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required

from machines.models import Machine
from workers.models import Worker

# Create your views here.
@login_required
def DashboardView(request, *args, **kwargs):
    return render(request, "dashboard/dashboard.html", {
        'workers': Worker.objects.all().order_by('-created'),
        'machines': Machine.objects.all()
    })