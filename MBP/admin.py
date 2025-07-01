from django.contrib import admin
from .models import Role, AppModel, PermissionType, RoleModelPermission, AuditLog

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('id',)
    ordering = ('name',)


@admin.register(AppModel)
class AppModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'app_label', 'slug')
    search_fields = ('name', 'app_label')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('id',)
    ordering = ('name',)


@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    readonly_fields = ('id',)
    ordering = ('name',)


@admin.register(RoleModelPermission)
class RoleModelPermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'model', 'permission_type')
    search_fields = ('role__name', 'model__name', 'permission_type__name')
    list_filter = ('role', 'model', 'permission_type')
    readonly_fields = ('id',)
    ordering = ('role',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'object_id')
    search_fields = ('user__email', 'action', 'model_name', 'object_id')
    list_filter = ('action', 'timestamp')
    readonly_fields = (
        'user', 'action', 'model_name', 'object_id', 'details',
        'old_data', 'new_data', 'ip_address', 'user_agent', 'timestamp'
    )
    ordering = ('-timestamp',)
