from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from MBP.models import AuditLog

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='login',
        details=f"User {user.full_name or user.email} logged in from {request.META.get("REMOTE_ADDR")}",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action='logout',
        details=f"User {user.full_name or user.email} logged out from {request.META.get("REMOTE_ADDR")}",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
    )
