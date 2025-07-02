from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Role, PermissionType, AppModel, RoleModelPermission, AuditLog
from MBP.permission import has_model_permission
from django.http import JsonResponse
import json
from MBP.utils import log_audit, safe_model_to_dict
from django.forms.models import model_to_dict
from django.db.models import Q
from dateutil.parser import parse as parse_datetime
from django.utils.timezone import now

def get_client_time(request):
    client_time_str = request.POST.get('client_time') or request.GET.get('client_time')
    if client_time_str:
        try:
            return parse_datetime(client_time_str)
        except Exception as e:
            print("Failed to parse client time:", e)
    return now()




@has_model_permission('Role', 'r')
def role_list_view(request):
    roles = Role.objects.annotate(user_count=Count('user'))

    paginator = Paginator(roles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch permissions for roles
    role_permissions = {}

    for role in roles:
        permissions = RoleModelPermission.objects.filter(role=role).select_related('model', 'permission_type')
        grouped = {}

        for perm in permissions:
            app_label = perm.model.app_label
            model_name = perm.model.name
            perm_name = perm.permission_type.name

            grouped.setdefault(app_label, {}).setdefault(model_name, []).append(perm_name)

        role_permissions[role.id] = grouped

    return render(request, 'role.html', {
        'page_obj': page_obj,
        'roles': page_obj.object_list,
        'role_permissions': role_permissions,
    })



@has_model_permission('Role', 'c')
def create_role_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if Role.objects.filter(name=name).exists():
            messages.error(request, "⚠️ Role with this name already exists.")
        else:
            new_role = Role.objects.create(name=name, description=description)
            time = get_client_time(request)
            log_audit(
                request.user, 'create', new_role,
                details=f"New Role Created: '{name}'",
                new_data=model_to_dict(new_role), request=request,
                timestamp=time)
            messages.success(request, "✅ Role created successfully.")
    return redirect('role_list')



@has_model_permission('Role', 'u')
def role_edit_view(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == 'POST':
        old_data = model_to_dict(role)
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('is_active') == 'True'

        if name:
            role.name = name
            role.description = description
            role.is_active = status
            role.save()
            time = get_client_time(request)
            log_audit(
                user=request.user,
                action='update',
                instance=role,
                details=f"Role Updated: '{role.name}'",
                old_data=old_data,
                new_data=model_to_dict(role),
                request=request,
                timestamp=time
            )
            messages.success(request, "✅ Role updated successfully.")
        else:
            messages.error(request, "❌ Role name is required.")

        return redirect('role_list')

    return redirect('role_list')




@has_model_permission('Role', 'd')
def role_delete_view(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    if request.user.role == role:
        messages.error(request, "❌ You cannot delete the role assigned to yourself.")
        return redirect('role_list')

    if request.method == 'POST':
        role.delete()
        time = get_client_time(request)
        log_audit(request.user, 'delete', role,
                  details="Role Deleted: '{}'".format(role.name),
                  new_data=model_to_dict(role), request=request, timestamp=time)
        messages.success(request, "🗑️ Role deleted successfully.")
    
    return redirect('role_list')



@has_model_permission('PermissionType', 'r')
def permission_type_list_view(request):
    permissions = PermissionType.objects.all().order_by('name')
    paginator = Paginator(permissions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'permission.html', {
        'page_obj': page_obj,
        'permissions': page_obj.object_list,
    })



@has_model_permission('PermissionType', 'c')
def create_permission_type_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip().lower() or (name[0].lower() if name else '')

        if not name:
            messages.error(request, "❌ Name is required.")
        elif PermissionType.objects.filter(name__iexact=name).exists():
            messages.error(request, "⚠️ A permission type with this name already exists.")
        elif PermissionType.objects.filter(code__iexact=code).exists():
            messages.error(request, f"⚠️ The code '{code}' already exists. Please use a different code.")
        else:
            new_permission = PermissionType.objects.create(name=name, code=code)
            time = get_client_time(request)
            log_audit(
                user=request.user,
                action='create',
                details=f"New Permission Created: '{name}'",
                instance=new_permission,
                new_data=model_to_dict(new_permission),
                request=request,
                timestamp=time
            )
            messages.success(request, "✅ Permission Type created successfully.")

    return redirect('permission_type_list')


@has_model_permission('PermissionType', 'u')
def permission_type_edit_view(request, type_id):
    permission_type = get_object_or_404(PermissionType, id=type_id)

    if request.method == 'POST':
        old_data = model_to_dict(permission_type)
        
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip().lower()
        is_active = request.POST.get('is_active') == 'True'

        if not name:
            messages.error(request, "❌ Name is required.")
            return redirect('permission_type_list')

        if PermissionType.objects.exclude(id=type_id).filter(name__iexact=name).exists():
            messages.error(request, f"⚠️ Name '{name}' already exists.")
        elif PermissionType.objects.exclude(id=type_id).filter(code__iexact=code).exists():
            messages.error(request, f"⚠️ Code '{code}' already exists.")
        else:
            permission_type.name = name
            permission_type.code = code or name[0].lower()
            permission_type.is_active = is_active
            permission_type.save()
            time = get_client_time(request)
            log_audit(
                user=request.user,
                action='update',
                instance=permission_type,
                details=f"Permission Updated: '{permission_type.name}'",
                old_data=old_data,
                new_data=model_to_dict(permission_type),
                request=request,
                timestamp=time
            )
            messages.success(request, "✅ Permission Type updated successfully.")
        
        return redirect('permission_type_list')

    return redirect('permission_type_list')



@has_model_permission('PermissionType', 'd')
def delete_permission_type_view(request, type_id):
    permission = get_object_or_404(PermissionType, id=type_id)

    if request.method == 'POST':
        permission.delete()
        time = get_client_time(request)
        log_audit(request.user, 'delete', permission,
                  details=f"Permission deleted: '{permission.name}'",
                  new_data=model_to_dict(permission), request=request, timestamp=time)

        messages.success(request, "🗑️ Permission Type deleted successfully.")

    return redirect('permission_type_list')


@has_model_permission('RoleModelPermission', 'r')
@require_GET
def get_role_permissions(request):
    role_id = request.GET.get('role_id')
    role_name = request.GET.get('role_name')

    role = None
    if role_id:
        role = get_object_or_404(Role, id=role_id)
    elif role_name:
        role = get_object_or_404(Role, name=role_name)

    apps = AppModel.objects.exclude(app_label__in=[
        'admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles'
    ])
    permissions = PermissionType.objects.all()
    assigned = RoleModelPermission.objects.filter(role=role)

    assigned_map = {
        (str(p.model.id), str(p.permission_type.id)): True
        for p in assigned
    }

    data = {
        'role': {
            'id': str(role.id),
            'name': role.name,
        },
        'apps': [],
        'permissions': [
            {
                'id': str(p.id),
                'name': p.name,
                'code': p.code
            }
            for p in permissions
        ],
    }

    for app in apps:
        data['apps'].append({
            'id': str(app.id),
            'name': app.name,
            'app_label': app.app_label,
            'verbose_name': app.verbose_name,
            'slug': app.slug,
            'permissions': [
                {
                    'permission_id': str(p.id),
                    'assigned': assigned_map.get((str(app.id), str(p.id)), False)
                } for p in permissions
            ]
        })

    return JsonResponse(data)

from django.core.exceptions import ObjectDoesNotExist

@has_model_permission('RoleModelPermission', 'c')
@csrf_exempt
@require_POST
def save_role_permissions(request):
    try:
        data = json.loads(request.body)
        role_id = data.get('role_id')
        model_id = data.get('model_id')
        permission_ids = data.get('permission_ids', [])

        if not role_id or not model_id:
            return JsonResponse({'error': 'Missing role_id or model_id'}, status=400)

        if not isinstance(permission_ids, list):
            return JsonResponse({'error': 'permission_ids must be a list'}, status=400)

        try:
            role = get_object_or_404(Role, id=role_id)
            model = get_object_or_404(AppModel, id=model_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid role or model ID'}, status=404)

        RoleModelPermission.objects.filter(role=role, model=model).delete()

        for pid in permission_ids:
            try:
                perm = PermissionType.objects.get(id=pid)
                new_permission = RoleModelPermission.objects.create(
                    role=role,
                    model=model,
                    permission_type=perm
                )

                time = get_client_time(request)
                log_audit(
                    user=request.user,
                    action='create',
                    details=f"New Model_Permission Created for Role: '{role.name}'",
                    instance=new_permission,
                    new_data=safe_model_to_dict(new_permission),
                    request=request,
                    timestamp=time
                )

            except PermissionType.DoesNotExist:
                continue

        return JsonResponse({'status': 'success'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e)}, status=500)



@has_model_permission('AuditLog', 'r')
def audit_log_list_view(request):
    search_query = request.GET.get('search', '').strip()
    action_filter = request.GET.get('log', '')
    logs = AuditLog.objects.select_related('user').order_by('-timestamp')

    if search_query:
        logs = logs.filter(
            Q(user__full_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    if action_filter:
        logs = logs.filter(action=action_filter)

    paginator = Paginator(logs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    actions = AuditLog.ACTION_CHOICES

    return render(request, 'auditlog.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'action_filter': action_filter,
        'actions': actions,
    })

@has_model_permission('AuditLog', 'd')
def delete_auditlog_view(request, log_id):
    log = get_object_or_404(AuditLog, id=log_id)

    if request.method == 'POST':
        log.delete()
        messages.success(request, "🗑️ Log deleted successfully.")
    return redirect('audit_log_list')