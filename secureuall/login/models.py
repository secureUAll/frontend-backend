from django.db import models
from django.contrib.auth.models import AbstractUser

from machines.models import MachineUser


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
    userType = (
        ('S', 'Subscriber'),
        ('O', 'Owner'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accessRequest')
    role = models.CharField(max_length=1, choices=userType, null=False, blank=False)
    motive = models.TextField()
    machines = models.TextField()  # Separated by semicollon
    created_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    notes = models.TextField()

    def get_machines(self):
        return [m.strip() for m in self.machines.split(";") if m]

    def get_status(self):
        if self.pending:
            return "Pending approval"
        elif not self.approved:
            return "Denied"
        return "Approved"

    class Meta:
        # can't have been approved and have status pending
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_if_approved_not_pending",
                check=(
                        models.Q(approved=True, pending=False) # Approved
                        | models.Q(approved=False, pending=True) # Denied
                        | models.Q(approved=False, pending=False) # Pending
                ),
            )
        ]