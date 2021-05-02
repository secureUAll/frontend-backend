from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class SecureuallUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='secureuallUser',
    )
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.name
