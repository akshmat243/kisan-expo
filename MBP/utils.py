from MBP.models import AuditLog
from django.forms.models import model_to_dict
from django.utils import timezone
import uuid
from datetime import datetime


def log_audit(user, action, instance, old_data=None, new_data=None, details="", request=None, timestamp=None):
    ip = request.META.get("REMOTE_ADDR") if request else None
    agent = request.META.get("HTTP_USER_AGENT") if request else None

    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=instance.__class__.__name__,
        object_id=str(instance.pk),
        details=details,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip,
        user_agent=agent,
        timestamp=timestamp or timezone.now()
    )


from django.db.models.fields.files import FieldFile
from decimal import Decimal
from datetime import timedelta


def safe_model_to_dict(instance):
    data = model_to_dict(instance)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
        elif isinstance(value, uuid.UUID):
            data[key] = str(value)
        elif isinstance(value, FieldFile):
            data[key] = value.url if value else None
        elif isinstance(value, Decimal):
            data[key] = float(value)  # Or use str(value) for exact precision
        elif hasattr(value, 'pk'):
            data[key] = str(value.pk)
    return data

def dev_time_now():
    return timezone.now() + timedelta(hours=5, minutes=30)