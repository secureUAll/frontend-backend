from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect

from secureuall.settings import PRODUCTION
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

# Create your views here.


class LoginView(View):
    template_name = "login/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')
        return render(request, self.template_name, {'production': PRODUCTION})

    def post(self, request, *args, **kwargs):
        # In development mode, register and authenticate user with given email
        if not request.user.is_authenticated and not PRODUCTION and request.POST and 'email' in request.POST and request.POST['email']:
            email = request.POST['email'].strip()
            # If does not exist, register on db
            if not User.objects.filter(email=email).exists():
                u = User.objects.create_user(email, email)
                u.first_name = "Utilizador de teste"
                u.save()
            else:
                u = User.objects.get(email=email)
            # Log in
            login(request, u)
            # If ?next= parameter is passed, redirect to requested page
            if 'next' in request.GET and request.GET['next']:
                return redirect(request.GET['next'])
            # Else, redirect to dashboard
            return redirect('dashboard:dashboard')
        return render(request, self.template_name, {'production': PRODUCTION})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        # In production, log out with saml2
        if PRODUCTION:
            return redirect('/saml2/logout/')
        # In development, log user out on Django only
        logout(request)
        return redirect('login:login')