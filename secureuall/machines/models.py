from django.db import models
from django.db.models import Q
from .validators import *
from model_utils import FieldTracker


class Machine(models.Model):
    riskLevelsOps = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    )
    scanLevelOps = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4)
    )
    periodicityOps = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly')
    )

    ip = models.CharField(max_length=15, null=True, blank=True, validators=[validate_ip])
    dns = models.CharField(max_length=255, null=True, blank=True, validators=[validate_dns])
    os = models.CharField(max_length=20, null=True, blank=True)
    risk = models.CharField(max_length=1, choices=riskLevelsOps, null=True, blank=True)
    scanLevel = models.CharField(max_length=1, choices=scanLevelOps, null=True, blank=True, default='2')
    location = models.CharField(max_length=30, null=True, blank=True)
    periodicity = models.CharField(max_length=1, choices=periodicityOps, default='W')
    nextScan = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tracker = FieldTracker()

    def __str__(self):
        if self.ip and self.dns:
            return f"{self.ip} / {self.dns}"
        return self.ip or self.dns

    class Meta:
        # must have ip or dns (or both)!
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_ip_and_or_dns",
                check=(
                        models.Q(ip__isnull=True, dns__isnull=False)
                        | models.Q(ip__isnull=False, dns__isnull=True)
                        | models.Q(ip__isnull=False, dns__isnull=False)
                ),
            )
        ]

    @staticmethod
    def is_ip(ip):
        return validate_ip(ip)

    @staticmethod
    def is_dns(dns):
        return validate_dns(dns)

    @staticmethod
    def exists(ip, dns):
        # Different machines must have different IPs/DNS
        # An IP can be shared by multiple machines if they have different DNS
        # A DNS can be shared by multiple machines if they have different IPs
        if dns and not ip and Machine.objects.filter(ip='', dns=dns).exists():
            return Machine.objects.filter(Q(Q(ip='') | Q(ip=None)) & Q(dns=dns))
        if ip and not dns and Machine.objects.filter(ip=ip, dns='').exists():
            return Machine.objects.filter(Q(Q(dns='') | Q(dns=None)) & Q(ip=ip))
        return Machine.objects.filter(ip=ip, dns=dns)

    def save(self, *args, **kwargs):
        """ Automatically add "modified" to update_fields."""
        update_fields = kwargs.get('update_fields')
        if update_fields is not None:
            kwargs['update_fields'] = set(update_fields) | {'modified'}
        super().save(*args, **kwargs)
        

class MachineUser(models.Model):
    userType = (
        ('S', 'Subscriber'),
        ('O', 'Owner'),
    )

    user = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='machines')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='users')
    userType = models.CharField(max_length=1, choices=userType)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "machine"),)


class MachineWorker(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='workers')
    worker = models.ForeignKey('workers.worker', on_delete=models.CASCADE, related_name='machines')


class Scan(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='scans')
    worker = models.ForeignKey('workers.Worker', on_delete=models.CASCADE, related_name='scans')
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=15)


class MachineService(models.Model):
    service = models.CharField(max_length=24)
    version = models.TextField()

    def _str_(self):
        return str(self.service) + " (" + str(self.version) + ")"

    class Meta:
        unique_together = (("service", "version"),)


class MachinePort(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='ports')
    port = models.IntegerField()
    service = models.ForeignKey(MachineService, on_delete=models.CASCADE)
    scanEnabled = models.BooleanField(default=True)
    vulnerable = models.BooleanField(default=False)

    def __str__(self):
        return str(self.service) + " (" + str(self.port) + ")"

    class Meta:
        unique_together = (("machine", "port", "scanEnabled"),)


class Vulnerability(models.Model):
    risk = models.IntegerField()
    type = models.CharField(max_length=12)
    description = models.CharField(max_length=256)
    location = models.TextField()
    status = models.CharField(max_length=12)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='vulnerabilities')
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name='vulnerabilities')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status_tracker = FieldTracker(fields=['status'])

    def __str__(self):
        return "(" + str(self.risk) + ") " + self.description


class VulnerabilityComment(models.Model):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Log(models.Model):
    cod = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='logs')
    worker = models.ForeignKey('workers.Worker', on_delete=models.CASCADE, related_name='logs')
    log = models.TextField()

