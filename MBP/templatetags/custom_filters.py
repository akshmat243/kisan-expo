from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


from MBP.models import AppModel, PermissionType, RoleModelPermission

@register.simple_tag
def has_perm(user, model_name, perm_code):
    if user.is_superuser:
        return True  # ✅ This line must be here
    role = getattr(user, 'role', None)
    if not role:
        return False
    try:
        model = AppModel.objects.get(name=model_name)
        perm = PermissionType.objects.get(code=perm_code)
    except (AppModel.DoesNotExist, PermissionType.DoesNotExist):
        return False
    return RoleModelPermission.objects.filter(role=role, model=model, permission_type=perm).exists()
