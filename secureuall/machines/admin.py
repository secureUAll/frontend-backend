from django.contrib import admin

from .models import Machine, MachineWorker, Vulnerability, MachineUser, Scan, MachinePort, Log


# Machine


class MachineWorkerInline(admin.TabularInline):
    model = MachineWorker
    extra = 0


class VulnerabilityInline(admin.TabularInline):
    model = Vulnerability
    extra = 0


class MachineUserInline(admin.TabularInline):
    model = MachineUser
    extra = 0


class ScanInline(admin.TabularInline):
    model = Scan
    extra = 0


class MachinePortInline(admin.TabularInline):
    model = MachinePort
    extra = 0


class LogInline(admin.TabularInline):
    model = Log
    extra = 0

class MachineAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'ip', 'dns', 'scanLevel', 'location', 'nextScan']
    list_filter = ['location', 'scanLevel', 'nextScan']
    inlines = [MachineWorkerInline, VulnerabilityInline, MachineUserInline, ScanInline, MachinePortInline, LogInline]


admin.site.register(Machine, MachineAdmin)


class MachineWorkerAdmin(admin.ModelAdmin):
    list_display = ['machine', 'worker']
    list_filter = ['machine', 'worker']


admin.site.register(MachineWorker, MachineWorkerAdmin)
