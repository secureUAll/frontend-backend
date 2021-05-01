from django.shortcuts import render

# Create your views here.
def DashboardView(request, *args, **kwargs):
    return render(request, "dashboard/dashboard.html", {})