import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings

from login.models import User
from .models import Worker
from machines.models import Machine, MachineWorker, Log

from machines.forms import MachineWorkerBatchInputForm, MachineForm, IPRangeForm
from django.forms import formset_factory

from login.validators import UserHasAccessMixin, UserIsAdminAccessMixin

from services.kakfa import KafkaService

# Create your views here.


class WorkersView(LoginRequiredMixin, UserIsAdminAccessMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'workers': Worker.objects.all().order_by('-created'),
            'machinesAdded': request.session['machinesAdded'] if 'machinesAdded' in request.session else None,
            'machinesWithoutWorker': Machine.objects.filter(workers=None).count(),
            'filter': request.GET.get('status') if 'status' in request.GET else None
        }
        # If status param, filter by status
        if 'status' in request.GET and any([request.GET.get('status') in s[0] for s in Worker.statusOps]):
            context['workers'] = context['workers'].filter(status=request.GET.get('status'))
        # Remove session data after adding to context
        if 'machinesAdded' in request.session:
            request.session['machinesAdded']=None
        return render(request, "workers/workers.html", context)


class WorkerOperationsView(LoginRequiredMixin, UserIsAdminAccessMixin, View):

    def post(self, request, id=None, *args, **kwargs):
        # Validate that worker with id exists
        if not Worker.objects.filter(id=id).exists():
            return HttpResponse(
                json.dumps({'error': 'Invalid worker!'}),
                content_type='application/json',
                status=400
            )
        # Make operations on worker
        w = Worker.objects.get(id=id)
        success = False
        if 'name' in request.POST and request.POST['name']:
            # Edit name
            if 'editName' in request.POST['name'] and 'value' in request.POST and request.POST['value']:
                w.name = request.POST['value']
                w.save()
                success = True
        # Return worker manipulated if success, else error
        if success:
            return HttpResponse(
                serializers.serialize('json', [Worker.objects.get(id=id)]),
                content_type='application/json'
            )
        return HttpResponse(
            json.dumps({'error': 'Invalid request!'}),
            content_type='application/json',
            status=400
        )


class AddMachinesView(LoginRequiredMixin, UserIsAdminAccessMixin, View):
    context = {}
    template_name = "workers/addMachines.html"
    edit = False
    mode = "batch"
    MachineFormSet = formset_factory(MachineForm, extra=0, can_delete=True)

    def get(self, request, id=None, *args, **kwargs):
        self.getContext(id)
        return render(request, self.template_name, self.context)

    def post(self, request, id=None, *args, **kwargs):
        self.getContext(id)
        # 1. Receive user input and create machines for validation (without saving to database)
        if 'mode' in request.POST and request.POST['mode']:
            valid = False
            if request.POST['mode'] == 'batch':
                # Build form, validate it and update context
                self.context['form'] = MachineWorkerBatchInputForm(request.POST)
                valid = self.context['form'].validate_custom(self.context['worker'])
                self.context.update(self.context['form'].cleaned_data)
            elif request.POST['mode'] == 'range':
                # Build form, validate it and update context
                self.context['form'] = IPRangeForm(request.POST)
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
                    # Get machine from db, if exists
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
                # Notify colector of changes (only on production)
                if settings.PRODUCTION:
                    KafkaService().send(topic='FRONTEND', key=b'UPDATE', value={'ID': self.context['worker'].id})
                return redirect('workers:workers')
        return render(request, self.template_name, self.context)

    def getContext(self, id):
        w = get_object_or_404(Worker, id=id)
        self.context = {
            'mode': self.mode,
            'form': MachineWorkerBatchInputForm() if self.mode=='batch' else IPRangeForm(),
            'title': 'Add machines',
            'worker': w,
            'add': not self.edit,
            'ignored': 0
        }

        if self.edit:
            self.context['formset'] = self.MachineFormSet(initial=[vars(m) for m in Machine.objects.filter(workers__worker=w).order_by('dns', 'ip')])
            self.template_name = "workers/editMachines.html"
            self.context['title'] = "Edit machines list"

    def test_func(self):
        return User.has_access(self.request.user)


class WorkerLogsView(LoginRequiredMixin, UserIsAdminAccessMixin, View):
    context = {}
    template_name = "workers/logs.html"
    machine = False

    def get(self, request, id=None, *args, **kwargs):
        self.getContext(id)
        return render(request, self.template_name, self.context)

    def getContext(self, id):
        m = None
        w = None
        if self.machine:
            m = get_object_or_404(Machine, id=id)
        else:
            w = get_object_or_404(Worker, id=id)
        self.context = {
            'title': 'Worker | Logs' if w else 'Machine | Logs',
            'worker': w,
            'machine': m,
            'logs': Log.objects.filter(worker=w).order_by('-date') if w else Log.objects.filter(machine=m).order_by('-date')
        }
