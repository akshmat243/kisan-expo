from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Notification, Profile


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

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('user__email', 'message')
    ordering = ('-timestamp',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'mobile', 'country', 'gender', 'dob', 'age', 'created_at', 'updated_at'
    )
    search_fields = ('user__email', 'user__username', 'mobile', 'country')
    list_filter = ('gender', 'country', 'created_at', 'updated_at')
    readonly_fields = ('age', 'created_at', 'updated_at')
    autocomplete_fields = ('user',)

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'image', 'bio')
        }),
        ('Contact Details', {
            'fields': ('mobile', 'address', 'country')
        }),
        ('Personal Info', {
            'fields': ('gender', 'dob', 'age')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )