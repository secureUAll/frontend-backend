from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

from login.models import User


class UserHasAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return User.has_access(self.request.user)

    def handle_no_permission(self):
        return redirect('login:welcome')


class UserIsAdminAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        return redirect('dashboard:dashboard')