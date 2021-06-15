from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import signals


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


class UserNotification(models.Model):
    notificationsTypes = (
        ('Microsoft Teams', 'https://teams.com/.*'),
        ('Email', '.*')
    )

    type = models.CharField(max_length=30, choices=notificationsTypes)
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    value = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        # can't have same notification type for same user
        unique_together = ('type', 'user')


def create_user_notification_email(sender, instance, **kwargs):
    if not UserNotification.objects.filter(type='Email', user=instance).exists():
        print("User created, signal activated to create UserNotification for email!")
        UserNotification.objects.create(
            type='Email',
            user=instance,
            value=instance.email
        )


# Create user notification email by default when User is created
signals.post_save.connect(create_user_notification_email, sender=User)