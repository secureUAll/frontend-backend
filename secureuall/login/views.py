from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect

from secureuall.settings import PRODUCTION
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
class LoginView(View):
    template_name = "login/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')
        return render(request, self.template_name, {'production': PRODUCTION})

    def post(self, request, *args, **kwargs):
        # In development mode, register and authenticate user with given email
        if not request.user.is_authenticated and not PRODUCTION and request.POST and 'email' in request.POST:
            email = request.POST['email']
            if not User.objects.filter(email=email).exists():
                u = User.objects.create_user(email)
                u.first_name = "Utilizador de teste"
                u.save()
            else:
                u = User.models.get(email=email)
            login(request, u)
        return render(request, self.template_name, {'production': PRODUCTION})