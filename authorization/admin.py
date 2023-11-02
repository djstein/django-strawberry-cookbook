from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = []
    fieldsets = BaseUserAdmin.fieldsets + (
        (_("Extra"), {"fields": ("email_verified",)}),
    )


admin.site.register(User, UserAdmin)
