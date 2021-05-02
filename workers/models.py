from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=12)
    status = models.CharField(max_length=12)
    failures = models.IntegerField()

    def _str_(self):
        return self.name


class WorkerScanComment(models.Model):
    scan = models.ForeignKey('machines.Scan', on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=256)
    user_cod = models.ForeignKey('login.SecureuallUser', on_delete=models.CASCADE, related_name='scanComments')

    def _str_(self):
        return self.comment
