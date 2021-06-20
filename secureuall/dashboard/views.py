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
    pielabels = []
    piedata = []
    piechart = {'1':[],'2':[], '3':[],'4':[], '5':[]}
    vulnsdata = []
    vulnslabels = []
    unresolved_vulns = []
    machines_updates = []
    machines_addrem = []

    vulnset = Vulnerability.objects.all().order_by('-scan')

    # Define piechart (% of Machines in a Risk Level) x and y axes values.
    machineset = Machine.objects.filter(active__exact=True).order_by('-created')
    for machine in machineset:
        # Ignore empty risks
        if machine.risk:
            if str(machine.risk) in piechart:
                piechart[machine.risk].append(machine)
            else:
                piechart[machine.risk].append(machine)
    
    pielabels = [x for x in piechart.keys()]
    piedata = [len(v) for v in piechart.values()]


    # Define vulnerabilities chart.
    for x in range(12):
        scans = Scan.objects.filter(date__exact=date.today()-timedelta(days=x))
        count_vulnerabilities = 0
        for scan in scans:
            if scan.vulnerabilities:
                vulns = Vulnerability.objects.filter(scan_id=scan.id)
                count_vulnerabilities+=len(vulns)
        vulnsdata.append(count_vulnerabilities)
        delta = timezone.now()-timedelta(days=x)
        print(delta)
        label = (str)(delta.day) + " "+ delta.strftime('%b')
        print(label)
        vulnslabels.append(label)
    vulnsdata.reverse()
    vulnslabels.reverse()
    print(vulnslabels)

    # Calculates number of weeks without vulnerabilities.
    scanset = Scan.objects.all().order_by('-date')
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

    
    # Filter subscribbed machines if logged user is not system admin
    if not request.user.is_superuser:
        machineset = machineset.filter(users__user__in=[request.user.id])


    # ALERTS
    alerts = {'workers': Worker.objects.filter(status='D'),
              'requests': list(UserAccessRequest.objects.filter(pending=True).order_by('-created_at')),
              'machines': Machine.objects.filter(active=True, workers__isnull=True), 'number': 0}
    alerts['number'] += 1 if alerts['workers'].exists() else 0
    alerts['number'] += 1 if alerts['machines'].exists() else 0
    alerts['number'] += 1 if len(alerts['requests']) else 0
        
    context = {
        'workers': Worker.objects.all().order_by('-created'),
        'machines': machineset,
        'ports': MachinePort.objects.all(),
        'vulnerabilities': vulnset,
        'scans': scanset,
        'weeks_without_vulnerabilities': weeks_without_vuln,
        'active_vulnerabilities': vulnset.filter(status=['Fixing', 'Not Fixed']),
        'pielabels': pielabels,
        'piedata': piedata,
        'vulnslabels': vulnslabels,
        'vulnsdata': vulnsdata,
        'unresolved_vulns': unresolved_vulns,
        'machines_updates': machines_updates,
        'machines_addrem': machines_addrem,
        'alerts': alerts
    }

    return render(request, "dashboard/dashboard.html", context)