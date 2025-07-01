from django.db import models
from django.utils.text import slugify
import uuid
from django.conf import settings

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AppModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    app_label = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    verbose_name = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.verbose_name:
            self.verbose_name = self.name.replace('_', ' ').title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.app_label}.{self.name}"


class PermissionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=1, blank=True, unique=True)  # e.g., c, r, u, d
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code and self.name:
            self.code = self.name.strip().lower()[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"


class RoleModelPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    model = models.ForeignKey(AppModel, on_delete=models.CASCADE)
    permission_type = models.ForeignKey(PermissionType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'model', 'permission_type')

    def __str__(self):
        return f"{self.role.name} — {self.model.name} [{self.permission_type.name}]"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('register', 'Register'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('read', 'Read'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    object_id = models.CharField(max_length=100, null=True, blank=True)
    details = models.TextField(blank=True, null=True)
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {self.user} | {self.action} | {self.model_name} ({self.object_id})"
