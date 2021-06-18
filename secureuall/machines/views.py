from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from kafka import KafkaProducer
from services.kakfa import KafkaService
from django.http import HttpResponse, Http404
import logging
import json
from django.core import serializers
import machines.dataContext as dataContext
from login.models import User
from login.validators import UserHasAccessMixin, UserIsAdminAccessMixin
from login.forms import UserAccessRequestApprovalForm, RequestAccessForm
from services.notify.notifyfactory import NotifyFactory
from .forms import MachineNameForm

from .models import Machine, MachineUser, Scan, MachineService, MachinePort, Vulnerability, VulnerabilityComment
from login.models import UserAccessRequest

from datetime import datetime, timedelta, date
from django.utils import timezone
from django.http import JsonResponse

logging.basicConfig(level=logging.DEBUG)
# Create your views here.


@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def MachinesView(request, id):
    # Check that user has access to machine
    if not request.user.is_admin and not id in request.user.machines.all().values_list('machine', flat=True):
        return redirect('dashboard:dashboard')

    # If has access, proceed
    barchart = {}
    machine_users_id = []
    machine_users= {'S':[],'O':[]}
    piechart = {'1':[],'2':[], '3':[],'4':[], '5':[], 'unclassified':[]}

    try:
        machine = Machine.objects.get(id=id)
        machine_users_id=machine.users.all().values_list("user", flat=True)
        
        if request.POST:
            if 'machine_scanlevel' in request.POST:
                machine.scanLevel = request.POST['machine_scanlevel']
                machine.save()
            if 'machine_periodicity' in request.POST:
                p = request.POST['machine_periodicity']
                if p=='Daily': machine.periodicity = 'D'
                if p=='Weekly': machine.periodicity = 'W'
                if p=='Monthly': machine.periodicity = 'M'
                machine.save()
            if 'scan_request' in request.POST:
                KafkaService().send('FRONTEND', key=b'SCAN', value={'ID': id})
                return JsonResponse({'status':'false','message':"Validation passed"}, status=200)
            if 'vuln_status' in request.POST:
                vuln = Vulnerability.objects.get(scan_id=request.POST['scan_id'], id=request.POST['vuln_id'])
                vuln.status = request.POST['vuln_status']
                vuln.save()
                return JsonResponse({'status':'false','message':"Validation passed"}, status=200) 
            if 'vuln_comment' in request.POST:
                VulnerabilityComment.objects.create(
                        vulnerability= Vulnerability.objects.get(id=request.POST['vuln_id_comment']),
                        user=request.user,
                        comment=request.POST['vuln_comment'],
                    )
                return JsonResponse({'status':'false','message':"Validation passed"}, status=200)
            if 'new_sub' in request.POST:
                u = None
                try:
                    u=User.objects.get(email=request.POST['new_sub'])
                except User.DoesNotExist:
                    u=User.objects.create_user(request.POST['new_sub'], request.POST['new_sub'])
                if not u.id in machine_users_id:
                    MachineUser.objects.create(
                        user=u, 
                        machine=machine,
                        userType=request.POST['user_role'],
                    )
                    UserAccessRequest.objects.create(
                        user=u,
                        role=request.POST['user_role'],
                        motive=request.POST['user_motive'],
                        machines=machine,
                        approved=True,
                        pending=False,
                        notes="Automatically approved by the host owner",
                        approvedby=request.user
                    )
                return JsonResponse({'status':'false','message':"Validation passed"}, status=200)
            if 'remove_user' in request.POST:
                remu = None
                try:
                    remu=User.objects.get(email=request.POST['remove_user'])
                    if remu.id in machine_users_id:
                        users = MachineUser.objects.filter(user=remu.id, machine=id)
                        for user in users: user.delete()
                except User.DoesNotExist:
                    print("user does not exist")


        machine_users_id=machine.users.all().values_list("user", flat=True)
        for u_id in machine_users_id:
            user = machine.users.get(user=u_id)
            machine_users[user.userType].append(User.objects.get(id=u_id).email)

        # get logged user machine subscription type if user is not a system admin ('superuser')
        if User.objects.get(id=request.user.id).is_superuser == 1: 
            user_type = "A"
        else: 
            user_type = machine.users.get(user=request.user.id).userType


        vulncomments_set = []
        users = []
        allvulns = []
        scanset = Scan.objects.filter(machine=id).order_by('-date')
        for scan in scanset:
            if scan.vulnerabilities.all():
                vulnset = Vulnerability.objects.filter(scan_id=scan.id)
                for vuln in vulnset:
                    if not vuln.comments.all()==None:
                        for comment in vuln.comments.all():
                            u = User.objects.get(id=comment.user_id)
                            if not u in users:
                                users.append(u)
                        vulncomments_set.append(vuln.comments.all())
                allvulns.append(vulnset)

        # THIS IS FOR CHARTS
        for vset in allvulns:
            print(vset.values())
            for v in vset:
                if v.risk == 0: piechart['unclassified'].append(v)
                else: piechart[str(v.risk)].append(v)

        context = {
            'machine': machine,
            'machine_users': machine_users,
            'vuln_comments': vulncomments_set,
            'users': users,
            'scanset': scanset,
            'logged_user': User.objects.get(id=request.user.id),
            'user_type': user_type,
            'pielabels': [x for x in piechart.keys()],
            'piedata': [len(v) for v in piechart.values()],
            'piechart': piechart,
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
        data = {'error': 'Invalid request! Check you have permission and try again.'}
        form = UserAccessRequestApprovalForm(request.POST)
        if form.is_valid() and self.request.user.is_admin:
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
            req.approvedby = self.request.user
            req.save()
            # Notify user that it has changed status
            # Through every notification type active
            for un in req.user.notifications.all():
                n = NotifyFactory.createNotification(un.type)
                n.heading(f"Hello {self.request.user.first_name},")
                if req.approved:
                    n\
                        .text(f"Your request to access {n.bold(str(len(req.get_machines())))} machines submitted {n.bold(req.created_at)} has been approved! &#128522;")\
                        .text("You can access the machines you were granted access at Secure(UA)ll dashboard.")
                else:
                    n\
                        .text(f"Your request to access {n.bold(str(len(req.get_machines())))} machines submitted {n.bold(req.created_at)} has been denied.")\
                        .text("You can check the motive and fill a new request at at Secure(UA)ll dashboard.")
                n.button(
                    url=''.join(['http://', get_current_site(self.request).domain, "/"]),
                    text='Dashboard'
                )
                print("Sending notification for ", un.value)
                n.send(subject='[Secure(UA)ll info] Your access request has been reviewed', recipient=un.value, preview='Your access request has been reviewed')
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
        # If user is not admin, filter by his requests
        if not self.request.user.is_admin:
            requests = requests.filter(user=self.request.user)
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
        # If request submitted, show feedback to user
        self.context['requestSuccess'] = self.request.session['requestSuccess'] if 'requestSuccess' in self.request.session else False
        if 'requestSuccess' in self.request.session:
            self.request.session['requestSuccess']=None


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