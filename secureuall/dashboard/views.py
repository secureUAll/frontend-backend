from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.decorators import login_required

from login.models import User
from machines.models import Machine, MachineUser, Subscription, Scan, MachineService, MachinePort, Vulnerability, VulnerabilityComment
from workers.models import Worker

from datetime import datetime, timedelta, date
from django.utils import timezone

# Create your views here.
@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def DashboardView(request, *args, **kwargs):
    pielabels = []
    piedata = []
    piechart = {}
    barlabels = []
    bardata = []
    barchart = {}
    vulnsdata = []
    vulnslabels = []
    active_vuln = 0
    fixed_vulns = []
    machines_updates = {}
    machines_addrem = {}
    

    # Define barchart (Vulnerabilities by Group) x and y axes values.
    vulnset = Vulnerability.objects.all().order_by('-scan')
    for vuln in vulnset:
        if vuln.type in barchart:
            value = barchart.get(vuln.type)+1
            barchart[vuln.type] = value
        else:
            barchart[vuln.type] = 1
        # Calculates total of active vulnerabilities.
        if vuln.status == "Not Fixed":
            active_vuln+=1
    for key in barchart.keys():
        barlabels.append(key)
    for value in barchart.values():
        bardata.append(value)


    # Define piechart (% of Machines in a Risk Level) x and y axes values.
    machineset = Machine.objects.filter(active__exact=True).order_by('-created')
    for machine in machineset:
        if machine.active:
            if machine.risk in piechart:
                value = piechart.get(machine.risk)+1
                piechart[machine.risk] = value
            else:
                piechart[machine.risk] = 1

    for key in piechart.keys():
        pielabels.append(key)
    for value in piechart.values():
        percentage = round((value*100)/len(machineset))
        piedata.append(percentage)


    # Calculates number of weeks without vulnerabilities.
    scanset = Scan.objects.all().order_by('-date')
    weeks_without_vuln = 0
    for scan in scanset:
        if scan.vulnerabilities:
            delta = (date.today()-scan.date)
            weeks_without_vuln = (int)((delta.days)/7)
            break


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
        label = (str)(delta.day) + " "+ delta.strftime('%b')
        vulnslabels.append(label)
    vulnsdata.reverse()
    vulnslabels.reverse()


    # Get fixed vulnerabilities from previous week
    scanset_updates = Scan.objects.filter(date__gte=timezone.now()-timedelta(days=7))
    for scan in scanset_updates:
        vulns = Vulnerability.objects.filter(scan_id=scan.id)
        for vuln in vulns:
            if vuln.updated != vuln.created and vuln.status_tracker.has_changed('status') and vuln.status == "Fixed":
                    if not vuln.machine in fixed_vulns:
                        machine = Machine.objects.filter(id=vuln.machine)
                        fixed_vulns.append(machine)


    # Get machines updates from previous week
    machineset_updates = Machine.objects.filter(updated__gte=timezone.now()-timedelta(days=7))
    for machine in machineset_updates:
        changes = machine.tracker.changed()
        if "os" in changes.keys(): machines_updates[machine] = "OS update"
        if "scanLevel" in changes.keys(): machines_updates[machine] = "scan level update"
        if "active" in changes.keys(): machines_addrem[machine] = machine.active
    machinuserset = MachineUser.objects.filter(created__gte=timezone.now()-timedelta(days=7))
    for machineUser in machinuserset:
        machine = machineUser.machine
        if machineUser.userType=='S':
            machines_updates[machine] = "subscriber added"
        elif machineUser.userType=='O':
            machines_updates[machine] = "owner added"

    context = {
        'workers': Worker.objects.all().order_by('-created'),
        'machines': machineset,
        'ports': MachinePort.objects.all(),
        'vulnerabilities': vulnset,
        'active_vulnerabilities': active_vuln,
        'scans': scanset,
        'weeks_without_vulnerabilities': weeks_without_vuln,
        'pielabels': pielabels,
        'piedata': piedata,
        'barlabels': barlabels,
        'bardata': bardata,
        'vulnsdata': vulnsdata,
        'vulslabels': vulnslabels,
        'fixed_vulns': fixed_vulns,
        'machines_updates': machines_updates,
        'machines_addrem': machines_addrem,
    }

    return render(request, "dashboard/dashboard.html", context)