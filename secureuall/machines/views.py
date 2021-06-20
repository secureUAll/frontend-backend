from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
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

from .models import Machine, MachineUser, Scan, MachineService, MachinePort, Vulnerability, VulnerabilityComment, Log, MachineChanges
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
    machine_users_id = []
    machine_users= {'S':[],'O':[]}
    piechart = {'1':[],'2':[], '3':[],'4':[], '5':[], 'unclassified':[]}
    linechart = {}
    vulncomments_set = []
    users = []
    allvulns = []
    scanset = Scan.objects.filter(machine=id).order_by('-date')
    count_vulns = 0
    scan_filter = "All scans"

    try:
        machine = Machine.objects.get(id=id)
        machine_users_id=machine.users.all().values_list("user", flat=True)



        # pie chart set up (vulnerabilities by risk)
        def get_piechartdata(vulns):
            count=0
            for vset in vulns:
                for v in vset:
                    if v.risk == 0: piechart['unclassified'].append(v)
                    else: piechart[str(v.risk)].append(v)
                    count+=1
            return count

        # get comments for vulnerabilities
        for scan in scanset:
            if scan.vulnerabilities.all():
                vulnset = Vulnerability.objects.filter(scan_id=scan.id)
                for vuln in vulnset:
                    # get comments for vulnerabilities
                    if not vuln.comments.all()==None:
                        for comment in vuln.comments.all():
                            u = User.objects.get(id=comment.user_id)
                            if not u in users:
                                users.append(u)
                        vulncomments_set.append(vuln.comments.all())
                allvulns.append(vulnset) # set of vulnerabilities for piechart
        
        # get data for line chart (vulnerabilities per scan)
        for scan in scanset:
            # adding to line chart
            if scan.status=='Done':
                label = (str)(scan.date.day) + " "+ scan.date.strftime('%b')
                if not scan.date in linechart.keys():
                    linechart[label] = scan.vulnerabilities.count()
                else: 
                    count = linechart[label]
                    count += scan.vulnerabilities.count()
                    linechart[label] = count

        # get data for pie chart (vulnerabilities by risk)
        count_vulns = get_piechartdata(allvulns)


        # POST requests from interface
        if request.POST:
            # Everyone
            if 'vuln_comment' in request.POST:
                VulnerabilityComment.objects.create(
                        vulnerability= Vulnerability.objects.get(id=request.POST['vuln_id_comment']),
                        user=request.user,
                        comment=request.POST['vuln_comment'],
                    )
                return JsonResponse({'status':'false','message':"Validation passed"}, status=200)
            elif 'vuln_status' in request.POST:
                vuln = Vulnerability.objects.get(scan_id=request.POST['scan_id'], id=request.POST['vuln_id'])
                vuln.status = request.POST['vuln_status']
                vuln.save()
                return JsonResponse({'status':'false','message':"Validation passed"}, status=200)
            elif ('last_scan' in request.POST) or ('last_month' in request.POST) or ('all_scans' in request.POST):
                req = list(request.POST)[1]
                scans = []
                count_vulns = 0
                if req == 'last_scan': 
                    scans = scanset[:1]
                    scan_filter = "Last scan"
                elif req == 'last_month': 
                    scans = scanset.filter(date__gte=timezone.now()-timedelta(days=30))
                    scan_filter = "Last month"
                elif req == 'all_scans':
                    scans = scanset
                    scan_filter = "All scans"
                allvulns = []
                for k in piechart.keys():
                    piechart[k] = []
                for scan in scans:
                    if scan.vulnerabilities.all:
                        vulnset = Vulnerability.objects.filter(scan_id=scan.id)
                        allvulns.append(vulnset)
                count_vulns = get_piechartdata(allvulns)
            # ADMIN and OWNER ONLY
            if request.user.is_admin or request.user.machines.all().filter(machine=machine, userType='O').exists():
                if 'machine_scanlevel' in request.POST:
                    machine.scanLevel = request.POST['machine_scanlevel']
                    machine.save()
                    changes = MachineChanges.objects.filter(machine=machine, type='S')
                    if not changes:
                        MachineChanges.objects.create(machine=machine, type='S')
                    else:
                        for mc in changes:
                            mc.save()
                elif 'machine_periodicity' in request.POST:
                    p = request.POST['machine_periodicity']
                    if p=='Daily': machine.periodicity = 'D'
                    if p=='Weekly': machine.periodicity = 'W'
                    if p=='Monthly': machine.periodicity = 'M'
                    machine.save()
                    changes = MachineChanges.objects.filter(machine=machine, type='P')
                    if not changes:
                        MachineChanges.objects.create(machine=machine, type='P')
                    else:
                        for mc in changes:
                            mc.save()
                elif 'scan_request' in request.POST:
                    # Validate that machine has workers
                    if not machine.workers.all().exists():
                        return JsonResponse({'status': False, 'message': "It is not possible to schedule a scan because this machine does not have a worker associated."}, status=200)
                    elif not machine.workers.all().exclude(status='D').exists():
                        return JsonResponse({'status': False, 'message': "It is not possible to schedule a scan because all workers that machine is associated with are down."}, status=200)
                    if settings.PRODUCTION:
                        KafkaService().send('FRONTEND', key=b'SCAN', value={'ID': id})
                    else:
                        return JsonResponse({'status': False, 'message': "Not in production! Can't schedule requests."}, status=500)
                    return JsonResponse({'status':True,'message':"Validation passed"}, status=200)
                elif 'new_sub' in request.POST:
                    u = None
                    try:
                        u=User.objects.get(email=request.POST['new_sub'].strip())
                    except User.DoesNotExist:
                        u=User.objects.create_user(request.POST['new_sub'].strip(), request.POST['new_sub'])
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
                elif 'remove_user' in request.POST:
                    remu = None
                    try:
                        remu=User.objects.get(email=request.POST['remove_user'])
                        if remu.id in machine_users_id:
                            musers = MachineUser.objects.filter(user=remu.id, machine=id)
                            for user in musers: user.delete()
                    except User.DoesNotExist:
                        print("user does not exist")
            else:
                return JsonResponse({'error': 'You don\'t have permissions to perform that operation.'}, status=401)


        # get list of users (owners and subscribers) of this machine
        machine_users_id=machine.users.all().values_list("user", flat=True)
        for u_id in machine_users_id:
            user = machine.users.get(user=u_id)
            machine_users[user.userType].append(User.objects.get(id=u_id).email)

        # get logged user machine subscription type if user is not a system admin ('superuser')
        if User.objects.get(id=request.user.id).is_superuser == 1: 
            user_type = "A"
        else: 
            user_type = machine.users.get(user=request.user.id).userType


        context = {
            'machine': machine,
            'machine_users': machine_users,
            'vuln_comments': vulncomments_set,
            'vulnerabilities': Vulnerability.objects.filter(machine_id=id).order_by('-created'),
            'users': users,
            'scanset': scanset,
            'logged_user': User.objects.get(id=request.user.id),
            'user_type': user_type,
            'pielabels': [x for x in piechart.keys()],
            'piedata': [len(v) for v in piechart.values()],
            'linelabels': [x for x in linechart.keys()][::-1],
            'linedata': [v for v in linechart.values()][::-1],
            'count_vulns': count_vulns,
            'scan_filter': scan_filter,
            'workersMachines': request.session['workersMachines'] if 'workersMachines' in request.session else None,
        }

        # Clean session vars
        if 'workersMachines' in request.session:
            request.session['workersMachines'] = None
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
                n.heading(f"Hello {req.user.first_name},")
                if req.approved:
                    n\
                        .text(f"Your request to access {n.bold(str(len(req.get_machines())))} hosts submitted {n.bold(req.created_at.strftime('%Y/%m/%d %H:%M'))} has been approved! &#128522;")\
                        .text("You can access the hosts you were granted access at Secure(UA)ll dashboard.")
                else:
                    n\
                        .text(f"Your request to access {n.bold(str(len(req.get_machines())))} hosts submitted {n.bold(req.created_at.strftime('%Y/%m/%d %H:%M'))} has been denied.")\
                        .text("You can check the motive and fill a new request at at Secure(UA)ll dashboard.")
                n.button(
                    url=''.join([settings.DEPLOY_URL, "/"]),
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


class LogView(LoginRequiredMixin, UserIsAdminAccessMixin, View):

    def get(self, request, id=None, *args, **kwargs):
        if Log.objects.filter(cod=id).exists():
            return HttpResponse(
                serializers.serialize('json', [Log.objects.get(cod=id)]),
                content_type='application/json'
            )
        return HttpResponse(
            json.dumps({'error': 'Log with given id does not exist!'}),
            content_type='application/json',
            status=400
        )


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