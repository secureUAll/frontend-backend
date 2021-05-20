from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()

    @staticmethod
    def has_access(user):
        if not user or not user.is_authenticated:
            return False
        return user.is_admin or user.machines.all().count()


class UserAccessRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accessRequest')
    motive = models.TextField()
    machines = models.TextField()  # Separated by semicollon
    created_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    notes = models.TextField()

    def get_machines(self):
        return self.machines.split(";")
