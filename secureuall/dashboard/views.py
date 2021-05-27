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
    context = {
        'workers': Worker.objects.all().order_by('-created'),
        'machines': Machine.objects.all()
    }
    # If user is not admin, filter data according to access permitions
    if not request.user.is_admin:
        context['workers'] = [],
        context['machines'] = context['machines'].filter(users__user=request.user)
    return render(request, "dashboard/dashboard.html", context)