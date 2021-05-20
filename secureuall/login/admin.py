from django.contrib import admin

from .models import User, UserAccessRequest

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_admin', 'is_superuser']


admin.site.register(User, UserAdmin)


class UserAccessRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'pending', 'approved']
    list_filter = ['user', 'pending', 'approved']


admin.site.register(UserAccessRequest, UserAccessRequestAdmin)