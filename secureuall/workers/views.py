from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import re

from .models import Worker
from machines.models import Machine

from machines.methods.machine import MachineHandler

# Create your views here.


class WorkersView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'workers': Worker.objects.all().order_by('-created'),
            'machinesAdded': request.session['machinesAdded'] if 'machinesAdded' in request.session else None
        }
        # Remove session data after adding to context
        if 'machinesAdded' in request.session:
            request.session['machinesAdded']=None
        return render(request, "workers/workers.html", context)


class AddMachinesView(LoginRequiredMixin, View):
    context = {}
    template_name = "workers/addMachines.html"

    def get(self, request, id=None, *args, **kwargs):
        self.getContext(id)
        return render(request, self.template_name, self.context)

    def post(self, request, id=None, *args, **kwargs):
        self.getContext(id)
        # 1. Receive user input and create machines for validation (without saving to database)
        if 'machinesList' in request.POST and 'machines' in request.POST and request.POST['machines']:
            self.context['machines'], self.context['ignored'] = MachineHandler.machinesFromInput(request.POST['machines'])
            # User input allows user to edit input
            self.context['userInput'] = request.POST['machines']
            # If some were valid, pass to step 2
            if len(self.context['machines']) > 0:
                self.template_name = "workers/editMachines.html"
        # 2. Process machines details form
        elif 'validateMachines' in request.POST and request.POST['validateMachines']:
            self.context['validated'] = True
            form = MachineHandler.gatherFormByNumber(request.POST)
            self.context['machines'], success = MachineHandler.machinesDetailsForm(form, self.context['worker'])
            # 3. Redirect to workers list on success
            if success:
                request.session['machinesAdded'] = {'worker':id, 'machines':len(self.context['machines'])}
                return redirect('workers:workers')
            self.template_name = "workers/editMachines.html"
        return render(request, self.template_name, self.context)

    def getContext(self, id):
        self.context = {
            'title': 'Add machines',
            'worker': Worker.objects.get(name=id),
            'add': True,
            'ignored': 0
        }
