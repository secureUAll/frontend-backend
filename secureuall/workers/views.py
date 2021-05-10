from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Worker
from machines.models import Machine, MachineWorker

from machines.forms import MachineWorkerBatchInputForm, MachineForm
from django.forms import formset_factory

# Create your views here.


class WorkersView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'workers': Worker.objects.all().order_by('-created'),
            'machinesAdded': request.session['machinesAdded'] if 'machinesAdded' in request.session else None,
            'machinesWithoutWorker': Machine.objects.filter(workers=None).count()
        }
        # Remove session data after adding to context
        if 'machinesAdded' in request.session:
            request.session['machinesAdded']=None
        return render(request, "workers/workers.html", context)


class AddMachinesView(LoginRequiredMixin, View):
    context = {}
    template_name = "workers/addMachines.html"
    edit = False
    MachineFormSet = formset_factory(MachineForm, extra=0, can_delete=True)

    def get(self, request, id=None, *args, **kwargs):
        self.getContext(id)
        return render(request, self.template_name, self.context)

    def post(self, request, id=None, *args, **kwargs):
        self.getContext(id)
        # 1. Receive user input and create machines for validation (without saving to database)
        if 'batch' in request.POST:
            # Build form, validate it and update context
            self.context['form'] = MachineWorkerBatchInputForm(request.POST)
            valid = self.context['form'].validate_custom(self.context['worker'])
            self.context.update(self.context['form'].cleaned_data)
            # If valid, proceed to step 2
            if valid:
                self.template_name = "workers/editMachines.html"
                self.context['formset'] = self.MachineFormSet(initial=[vars(m) for m in self.context['machines']])
        # 2. Process machines details form
        elif 'validateMachines' in request.POST and request.POST['validateMachines']:
            self.template_name = "workers/editMachines.html"
            # Build form with inserted data
            self.context['formset'] = self.MachineFormSet(request.POST)
            valid = self.context['formset'].is_valid()
            if valid:
                # Store session data for success feedback on workers list
                request.session['machinesAdded'] = {'worker': id, 'machines': 0, 'new': 0, 'edited': 0, 'disassociated': 0}
                # Same form to db
                for f in self.context['formset']:
                    f = f.cleaned_data
                    # Get machine to db, if exists
                    mach = Machine.objects.get(id=f['id']) if Machine.objects.filter(id=f['id']).exists() else None
                    # If not for delete
                    if not f['DELETE']:
                        # If exists, update dns and ip
                        if mach:
                            mach.dns = f['dns']
                            mach.ip = f['ip']
                            request.session['machinesAdded']['edited'] += 1
                        # Else, create it
                        else:
                            mach = Machine.objects.create(ip=f['ip'], dns=f['dns'])
                            request.session['machinesAdded']['new'] += 1
                        # Edit attributes
                        mach.scanLevel = f['scanLevel']
                        mach.periodicity = f['periodicity']
                        mach.location = f['location']
                        mach.save()
                    # Associate to worker
                    if mach and not f['DELETE'] and not MachineWorker.objects.filter(worker=self.context['worker'], machine=mach).exists():
                        MachineWorker.objects.create(worker=self.context['worker'], machine=mach)
                        request.session['machinesAdded']['machines'] += 1
                    # If exists and to disassociate, remove MachineWorker
                    elif mach and f['DELETE'] and MachineWorker.objects.filter(worker=self.context['worker'], machine=mach).exists():
                        MachineWorker.objects.filter(worker=self.context['worker'], machine=mach).delete()
                        request.session['machinesAdded']['disassociated'] += 1
                return redirect('workers:workers')
        return render(request, self.template_name, self.context)

    def getContext(self, id):
        w = Worker.objects.get(name=id)
        self.context = {
            'form': MachineWorkerBatchInputForm(),
            'title': 'Add machines',
            'worker': w,
            'add': not self.edit,
            'ignored': 0
        }

        if self.edit:
            self.context['formset'] = self.MachineFormSet(initial=[vars(m) for m in Machine.objects.filter(workers__worker=w).order_by('dns', 'ip')])
            self.template_name = "workers/editMachines.html"
            self.context['title'] = "Edit machines list"

