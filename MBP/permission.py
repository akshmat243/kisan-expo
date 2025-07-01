from django.core.exceptions import PermissionDenied
from functools import wraps
from .models import AppModel, PermissionType, RoleModelPermission

def has_model_permission(model_name: str, permission_code: str):
    """
    Decorator to check if the current user has the specified model permission.
    Usage:
        @has_model_permission('Account', 'r')  # read permission on Account model
        def view_func(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            role = getattr(request.user, 'role', None)
            if not role:
                raise PermissionDenied("❌ No role assigned.")

            try:
                model = AppModel.objects.get(name=model_name)
                perm = PermissionType.objects.get(code=permission_code, is_active=True)
            except AppModel.DoesNotExist:
                raise PermissionDenied(f"❌ Model '{model_name}' does not exist.")
            except PermissionType.DoesNotExist:
                raise PermissionDenied(f"❌ Permission code '{permission_code}' is inactive or invalid.")

            if not RoleModelPermission.objects.filter(role=role, model=model, permission_type=perm).exists():
                raise PermissionDenied("🚫 You do not have the required permission.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
