from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect

from secureuall.settings import PRODUCTION
from login.models import User
from django.contrib.auth import login, logout

from machines.forms import MachineNameForm
from .forms import RequestAccessForm

from .models import UserAccessRequest

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
            login(request, u, backend='django.contrib.auth.backends.ModelBackend')
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


class WelcomeView(LoginRequiredMixin, View):
    context = {}
    template_name = "login/welcome.html"
    MachineNameFormSet = formset_factory(MachineNameForm, min_num=1, extra=5)

    def get(self, request, *args, **kwargs):
        # If user has access, redirect to home
        if User.has_access(self.request.user):
            return redirect('dashboard:dashboard')
        self.getcontext()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.getcontext()
        # 1. Validate request access form
        self.context['formMachines'] = self.MachineNameFormSet(request.POST)
        valid = self.context['formMachines'].is_valid() and self.context['formRequest'].is_valid()
        print("machines valid?", self.context['formMachines'].is_valid())
        print("formMachines", self.context['formMachines'].total_form_count())
        print("request valid?", self.context['formRequest'].is_valid())
        print("formRequest", self.context['formRequest'].cleaned_data)
        if valid:
            print("VALID")
            # Compute machines list
            machines = ""
            for f in self.context['formMachines']:
                if 'name' in f.cleaned_data:
                    machines += f.cleaned_data['name'] + ";"
            # Save request to the db
            UserAccessRequest.objects.create(
                user=self.request.user,
                motive=self.context['formRequest'].cleaned_data['motive'],
                machines=machines,
                role=self.context['formRequest'].cleaned_data['role']
            )
            request.session['requestSuccess'] = True
            return redirect('login:welcome')
        return render(request, self.template_name, self.context)

    def getcontext(self):
        # Build context
        initialformrequest = {'motive': ''} if not self.request.POST else self.request.POST.copy()
        initialformrequest['email'] = self.request.user.email
        print("INITIAL", initialformrequest)

        self.context = {
            'formRequest': RequestAccessForm(initial=initialformrequest) if not self.request.POST else RequestAccessForm(initialformrequest),
            'formMachines': self.MachineNameFormSet(initial=[]),
            'requests': {
                'pending': UserAccessRequest.objects.filter(user=self.request.user, pending=True),
            },
            'requestSubmitted': self.request.session['requestSuccess'] if 'requestSuccess' in self.request.session else None
        }
        # Clear request session
        if 'requestSuccess' in self.request.session: self.request.session['requestSuccess']=None
