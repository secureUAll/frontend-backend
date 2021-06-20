from django.contrib import admin

from .models import Machine, MachineWorker, Vulnerability, MachineUser, Scan, MachinePort, Log, MachineService, MachineChanges


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


class MachineChangesInline(admin.TabularInline):
    model = MachineChanges
    extra = 0

class MachineAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'ip', 'dns', 'active', 'scanLevel', 'location', 'nextScan']
    list_filter = ['location', 'scanLevel', 'nextScan', 'workers']
    inlines = [MachineWorkerInline, VulnerabilityInline, MachineUserInline, ScanInline, MachinePortInline, LogInline, MachineChangesInline]


admin.site.register(Machine, MachineAdmin)


class MachineWorkerAdmin(admin.ModelAdmin):
    list_display = ['machine', 'worker']
    list_filter = ['machine', 'worker']


admin.site.register(MachineWorker, MachineWorkerAdmin)


admin.site.register(MachineService)


class LogAdmin(admin.ModelAdmin):
    list_display = ['worker', 'machine', 'date']
    list_filter = ['worker', 'machine', 'date']


admin.site.register(Log, LogAdmin)


class ScanAdmin(admin.ModelAdmin):
    list_display = ['worker', 'machine', 'status', 'date']
    list_filter = list_display

admin.site.register(Scan, ScanAdmin)