from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from deuse_formation.admin import admin_site


@admin.register(get_user_model(), site=admin_site)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = [
        (
            None,
            {
                'fields': ['email', 'password', 'first_name', 'last_name']
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']
            }
        ),
        (
            _('Dates importantes'),
            {
                'fields': ['last_login', 'date_joined']
            }
        )
    ]
    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['email', 'password1', 'password2'],
            }
        ),
    ]
    list_display = ['email', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email']
    ordering = ['email']
