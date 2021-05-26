from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.decorators import login_required

from login.models import User
from machines.models import Machine
from workers.models import Worker

# Create your views here.
@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def DashboardView(request, *args, **kwargs):
    return render(request, "dashboard/dashboard.html", {
        'workers': Worker.objects.all().order_by('-created'),
        'machines': Machine.objects.all()
    })