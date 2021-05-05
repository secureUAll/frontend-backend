from django.db import models


class Machine(models.Model):
    riskLevelsOps = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    )
    scanLevelOps = (
        ('2', 2),
        ('3', 3),
        ('4', 4)
    )
    periodicityOps = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly')
    )

    ip = models.CharField(max_length=15, null=True, blank=True)
    dns = models.TextField(max_length=255, null=True, blank=True)
    os = models.CharField(max_length=20, null=True, blank=True)
    risk = models.CharField(max_length=1, choices=riskLevelsOps, null=True, blank=True)
    scanlevel = models.IntegerField(max_length=1, choices=scanLevelOps, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    periodicity = models.CharField(max_length=1, choices=periodicityOps, default='W')
    nextScan = models.DateField(auto_now_add=True)

    def _str_(self):
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


class MachineUser(models.Model):
    user = models.ForeignKey('login.SecureuallUser', on_delete=models.CASCADE, related_name='machines')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='users')
    userType = models.ForeignKey('login.UserType', on_delete=models.CASCADE, related_name='machineUsers')

    class Meta:
        unique_together = (("user", "machine"),)


class MachineWorker(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='workers')
    worker = models.ForeignKey('workers.worker', on_delete=models.CASCADE, related_name='machines')

class Subscription(models.Model):
    user = models.ForeignKey('login.SecureuallUser', on_delete=models.CASCADE, related_name='subscriptions')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='subscriptions')
    notificationEmail = models.CharField(max_length=50)
    description = models.CharField(max_length=256)

    def _str_(self):
        return self.description


class Scan(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='scans')
    worker = models.ForeignKey('workers.Worker', on_delete=models.CASCADE, related_name='scans')
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=15)


class MachineService(models.Model):
    service = models.CharField(max_length=24)
    version = models.CharField(max_length=12)

    def _str_(self):
        return self.service + " (" + str(self.version) + ")"

    class Meta:
        unique_together = (("service", "version"),)


class MachinePort(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='ports')
    port = models.IntegerField()
    service = models.ForeignKey(MachineService, on_delete=models.CASCADE)

    def _str_(self):
        return self.service + " (" + str(self.port) + ")"

    class Meta:
        unique_together = (("machine", "port"),)


class Vulnerability(models.Model):
    risk = models.IntegerField()
    type = models.CharField(max_length=12)
    description = models.CharField(max_length=256)
    location = models.CharField(max_length=30)
    status = models.CharField(max_length=12)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='vulnerabilities')

    def _str_(self):
        return "(" + self.risk + ") " + self.description


class VulnerabilityComment(models.Model):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('login.SecureuallUser', on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=256)

    def _str_(self):
        return self.comment


class Log(models.Model):
    cod = models.BigAutoField(primary_key=True)
    date = models.DateField() # auto_now=True
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='logs')
    worker = models.ForeignKey('workers.Worker', on_delete=models.CASCADE, related_name='logs')
    path = models.CharField(max_length=256) #caminho para o ficheiro de logs
