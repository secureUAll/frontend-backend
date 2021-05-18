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
