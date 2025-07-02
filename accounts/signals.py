from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from MBP.models import AuditLog
from django.utils.dateparse import parse_datetime
from django.utils import timezone


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    
    client_time_str = request.POST.get("client_time")
    client_time = parse_datetime(client_time_str) if client_time_str else timezone.now()
    AuditLog.objects.create(
        user=user,
        action='login',
        details=f"User {user.full_name or user.email} logged in from {request.META.get("REMOTE_ADDR")}",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
        timestamp=client_time
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    
    client_time_str = request.POST.get("client_time")
    client_time = parse_datetime(client_time_str) if client_time_str else timezone.now()
    AuditLog.objects.create(
        user=user,
        action='logout',
        details=f"User {user.full_name or user.email} logged out from {request.META.get("REMOTE_ADDR")}",
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
        timestamp=client_time
    )
