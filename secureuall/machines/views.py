from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from kafka import KafkaProducer
from django.http import HttpResponse, Http404
import logging
import json
from django.core import serializers
import machines.dataContext as dataContext
from login.models import User
from login.validators import UserHasAccessMixin
from login.forms import UserAccessRequestApprovalForm
from .forms import MachineNameForm

from .models import Machine, MachineUser, Subscription, Scan, MachineService, MachinePort, Vulnerability, VulnerabilityComment
from login.models import UserAccessRequest

logging.basicConfig(level=logging.DEBUG)
# Create your views here.


@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def MachinesView(request, id):
    try:
        machine = Machine.objects.get(id=id)
        context = {
            'machine': machine
        }
    except Machine.DoesNotExist:
        raise Http404('Machine does not exist')
    return render(request, "machines/machines.html", context)


class RequestsView(LoginRequiredMixin, UserHasAccessMixin, View):
    context = {}
    template_name = "machines/requests.html"

    def get(self, request, *args, **kwargs):
        self.getContext()
        return render(request, "machines/requests.html", self.context)

    def post(self, request, *args, **kwargs):
        print("POST to requests:", request.POST)
        form = UserAccessRequestApprovalForm(request.POST)
        if form.is_valid():
            req = UserAccessRequest.objects.get(id=form.cleaned_data['request'])
            # If approved, associate user to machines
            if form.cleaned_data['approve']:
                # For each machine, process it (ignore invalid names)
                for m in req.get_machines():
                    mform = MachineNameForm({'name': m})
                    if not mform.is_valid(): continue
                    print(m, mform.cleaned_data)
                    # If machine does not exist, create it
                    machinedb = mform.cleaned_data['machine']
                    if not machinedb:
                        if 'ip' in mform.cleaned_data and mform.cleaned_data['ip']:
                            machinedb = Machine.objects.create(ip=mform.cleaned_data['ip'])
                        elif 'dns' in mform.cleaned_data and mform.cleaned_data['dns']:
                            machinedb = Machine.objects.create(dns=mform.cleaned_data['dns'])
                    # Associate to user
                    MachineUser.objects.create(user=req.user, machine=machinedb, userType=req.role)
            # Change request status
            req.pending = False
            req.approved = form.cleaned_data['approve']
            req.notes = form.cleaned_data['notes']
            req.save()
            # Compute JSON answer
            data = {'request': form.cleaned_data['request'], 'approve': form.cleaned_data['approve']}
        else:
            data = {'error': 'There was an error processing the form, please try again.'}
        print("form valid?", form.is_valid())
        print("form", form.cleaned_data)
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',
            status=400 if 'error' in data else 200
        )

    def getContext(self):
        # Build context with request parameters
        requests = UserAccessRequest.objects.all()
        filter = self.request.GET.get('filter') if 'filter' in self.request.GET and self.request.GET['filter'] else 'pending'
        print("FILTER", filter)
        if filter == 'pending':
            requests = requests.filter(pending=True)
        elif filter == 'approved':
            requests = requests.filter(pending=False, approved=True)
        elif filter == 'denied':
            requests = requests.filter(pending=False, approved=False)
        self.context['requests'] = requests.order_by('pending')
        self.context['filter'] = filter



@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def kafka_test(request):
    producer = KafkaProducer(bootstrap_servers='kafka:9092',
                            security_protocol='SASL_SSL',
                            ssl_cafile='certs/CARoot.pem',
                            ssl_certfile='certs/certificate.pem',
                            ssl_keyfile='certs/key.pem',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username='django',
                            sasl_plain_password='django',
                            ssl_check_hostname=False,
                            api_version=(2,7,0),
                            value_serializer=lambda m: json.dumps(m).encode('latin'))

    producer.send('FRONTEND', key=b'SCAN', value={"MACHINE":"127.0.1.3"})
    producer.flush()
    return HttpResponse(200)