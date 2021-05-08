from django.contrib import admin

from .models import Worker
from machines.models import MachineWorker

# Machine


class MachineWorkerInline(admin.TabularInline):
    model = MachineWorker
    extra = 0


class WorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'failures']
    list_filter = ['status']
    inlines = [MachineWorkerInline]


admin.site.register(Worker, WorkerAdmin)