from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from authentication.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

# admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = [
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'client',
        'client_rep',
        'admin',
        'is_active',
        'updated_at'
    ]
    list_filter = ['admin', 'is_active', 'client_rep']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('client', 'client_rep', 'admin', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password', 'password2')}),
    )
    search_fields = ['email', 'phone_number']
    ordering = ['email', 'is_active']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
