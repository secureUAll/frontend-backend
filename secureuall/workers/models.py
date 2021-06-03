from django.db import models


class Worker(models.Model):
    statusOps = (
        ('I', 'Idle'),
        ('A', 'Active'),
        ('D', 'Down'),
    )

    name = models.CharField(max_length=12)
    status = models.CharField(max_length=1, choices=statusOps, default='I')
    failures = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkerScanComment(models.Model):
    scan = models.ForeignKey('machines.Scan', on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    user_cod = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='scanComments')

    def __str__(self):
        return self.comment
