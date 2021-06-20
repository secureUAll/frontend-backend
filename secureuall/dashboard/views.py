from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.decorators import login_required
from django.db.models import Q

from login.models import User, UserAccessRequest
from machines.models import Machine, MachineUser, Scan, MachineService, MachinePort, Vulnerability, VulnerabilityComment, MachineChanges
from workers.models import Worker

from datetime import datetime, timedelta, date
from django.utils import timezone
import random


# Create your views here.
@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def DashboardView(request, *args, **kwargs):
    piechart = {'1':[],'2':[], '3':[],'4':[], '5':[], 'unclassified':[]}
    vulnsdata = []
    vulnslabels = []
    unresolved_vulns = []
    machines_updates = []
    machines_addrem = []

    vulnset = Vulnerability.objects.all().order_by('-scan')

    # Filter subscribbed machines if logged user is not system admin
    if not request.user.is_admin:
        machineset = Machine.objects.filter(users__user__in=[request.user.id])
    else:
        machineset = Machine.objects.filter(active__exact=True).order_by('-created')

    # Define piechart (% of Machines in a Risk Level)
    def get_piechartdata(mset):
        for machine in mset:
            # Ignore empty risks
            if machine.risk:
                if machine.risk=='0':
                    piechart['unclassified'].append(machine)
                else:
                    piechart[str(machine.risk)].append(machine)

    # get data for pie chart (vulnerabilities by risk)
    get_piechartdata(machineset)

    # Define banner chart with vulnerabilities
    for x in range(12):
        scans = Scan.objects.filter(date__exact=date.today()-timedelta(days=x))
        count_vulnerabilities = 0
        for scan in scans:
            if scan.vulnerabilities:
                vulns = Vulnerability.objects.filter(scan_id=scan.id)
                count_vulnerabilities+=len(vulns)
        vulnsdata.append(count_vulnerabilities)
        delta = timezone.now()-timedelta(days=x)
        label = (str)(delta.day) + " "+ delta.strftime('%b')
        vulnslabels.append(label)


    # Calculates number of weeks without vulnerabilities general
    if not request.user.is_admin:
        scanset = Scan.objects.all().order_by('-date')
    else:
        scanset = Scan.objects.filter(machine_id__in=[m.id for m in machineset]).order_by('-date')
    weeks_without_vuln = 0
    for scan in scanset:
        if scan.vulnerabilities:
            delta = (date.today()-scan.date)
            weeks_without_vuln = (int)((delta.days)/7)
            break


    # CARDS UPDATES
    # Get machines added and removed from previous week
    machines_addrem = Machine.objects.filter(Q(active=False, updated__gte=timezone.now()-timedelta(days=7)) | Q(created__gte=timezone.now()-timedelta(days=7))).order_by('-updated')
    
    # Get unresolved vulnerabilities from previous week
    unresolved_vulns = Vulnerability.objects.filter(Q(created__gte=timezone.now()-timedelta(days=7)) | Q(updated__gte=timezone.now()-timedelta(days=7)))

    # Get machines updates from previous week
    machines_updates = MachineChanges.objects.filter(created__gte=timezone.now()-timedelta(days=7), updated__gte=timezone.now()-timedelta(days=7))


    # ALERTS
    alerts = {
        'workers': Worker.objects.filter(status='D'),
        'requests': list(UserAccessRequest.objects.filter(pending=True).order_by('-created_at')),
        'machines': Machine.objects.filter(active=True, workers__isnull=True) if Worker.objects.all() else Machine.objects.filter(id=9876567), # TODO Remove later
        'noworkers': not Worker.objects.all().exists(),
        'number': 0
  }
    alerts['number'] += 1 if alerts['workers'].exists() else 0
    alerts['number'] += 1 if alerts['machines'].exists() else 0
    alerts['number'] += 1 if len(alerts['requests']) else 0
    alerts['noworkers'] += 1 if alerts['noworkers'] else 0
        
    context = {
        'workers': Worker.objects.all().order_by('-created'),
        'machines': machineset,
        'ports': MachinePort.objects.filter(machine_id__in=[m.id for m in machineset]),
        'vulnerabilities': vulnset.filter(machine_id__in=[m.id for m in machineset]),
        'scans': scanset.filter(machine_id__in=[m.id for m in machineset]),
        'weeks_without_vulnerabilities': weeks_without_vuln,
        'active_vulnerabilities': vulnset.filter(status__in=['Fixing', 'Not Fixed'], machine_id__in=[m.id for m in machineset]),
        'pielabels': [x for x in piechart.keys()],
        'piedata': [len(v) for v in piechart.values()],
        'vulnslabels': vulnslabels[::-1],
        'vulnsdata': vulnsdata[::-1],
        'unresolved_vulns': unresolved_vulns,
        'machines_updates': machines_updates,
        'machines_addrem': machines_addrem,
        'alerts': alerts,
    }

    return render(request, "dashboard/dashboard.html", context)