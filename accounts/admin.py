from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'full_name', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'role')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    fieldsets = (
        (None,                {'fields': ('email', 'password')}),
        ('Personal Info',     {'fields': ('full_name', 'role')}),
        ('Permissions',       {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates',   {'fields': ('last_login', 'date_joined')}),
        ('Creator',           {'fields': ('created_by',)}),
    )
    readonly_fields = ('last_login', 'date_joined', 'created_by')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_superuser:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
