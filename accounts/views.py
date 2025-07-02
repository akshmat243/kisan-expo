from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from MBP.permission import has_model_permission
from django.contrib import messages
from .models import User, Role
from MBP.models import AuditLog
from .forms import UserRegisterForm, EmailLoginForm, UserCreateForm
from MBP.utils import log_audit
from MBP.utils import safe_model_to_dict
from django.utils.timezone import now
from dateutil.parser import parse as parse_datetime

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def get_client_time(request):
    client_time_str = request.POST.get('client_time') or request.GET.get('client_time')
    if client_time_str:
        try:
            return parse_datetime(client_time_str)
        except Exception as e:
            print("Failed to parse client time:", e)
    return now()


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            time = get_client_time(request)
            AuditLog.objects.create(
                user=user,
                action='register',
                model_name='User',
                object_id=str(user.id),
                details=f"User '{user.full_name}' registered.",
                new_data={
                    "username": user.full_name,
                    "email": user.email,
                },
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                timestamp=time
            )
            messages.success(request, "✅ Registration successful! Please wait for admin approval.")
            return redirect('login')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = EmailLoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if not user.is_active:
                    messages.error(request, "Your account is not active. Please wait for admin approval.")
                    return redirect('login')

                if hasattr(user, 'role') and user.role and not user.role.is_active:
                    messages.error(request, "Your role is inactive. Contact the admin.")
                    return redirect('login')
                
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def dashboard_view(request):
    return render(request, 'base.html')




@has_model_permission('User', 'r')
def user_list_view(request):
    search = request.GET.get('search', '')
    role = request.GET.get('role', '')
    status = request.GET.get('status', '')
    page_number = request.GET.get('page', 1)

    if request.user.is_superuser:
        users = User.objects.all()
    else:
        users = User.objects.filter(created_by=request.user)
        
    user_role = getattr(request.user, 'role', None)

    if request.user.is_superuser:
        roles = Role.objects.all()
    elif user_role:
        roles = Role.objects.exclude(id=user_role.id)
    else:
        roles = Role.objects.none()

    if search:
        users = users.filter(full_name__icontains=search) | users.filter(email__icontains=search)

    if role:
        users = users.filter(role_id=role)

    if status == 'True':
        users = users.filter(is_active=True)
    elif status == 'False':
        users = users.filter(is_active=False)

    paginator = Paginator(users, 5)
    page_obj = paginator.get_page(page_number)
    
    # roles = Role.objects.all()
    return render(request, 'users.html', {
        'users': page_obj.object_list,
        'page_obj': page_obj,
        'roles': roles,
        'search': search,
        'role': role,
        'status': status
    })



@has_model_permission('User', 'c')
def user_create_view(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.created_by = request.user
            user.is_active = True
            user.save()
            time = get_client_time(request)
            log_audit(
                user=request.user,
                action='create',
                instance=user,
                details=f"New User Created: '{user.full_name}'",
                new_data=safe_model_to_dict(user),
                request=request,
                timestamp=time
            )
            messages.success(request, '✅ User created successfully.')
            return redirect('user_list')
        else:
            messages.error(request, '⚠️ Please correct the errors below.')
            return redirect('user_list')
    return redirect('user_list')


@has_model_permission('User', 'u')
def user_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        old_data = user
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        role_id = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'True'
        password = request.POST.get('password')

        if email != user.email and User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, '⚠️ Email already exists.')
            return redirect('user_list')

        user.full_name = full_name
        user.email = email
        user.role_id = role_id
        user.is_active = is_active
        if password:
            user.set_password(password)
        user.save()
        time = get_client_time(request)
        log_audit(
                user=request.user,
                action='update',
                instance=user,
                details=f"User Updated: '{user.full_name}'",
                old_data=safe_model_to_dict(old_data),
                new_data=safe_model_to_dict(user),
                request=request,
                timestamp=time
            )

        messages.success(request, '✅ User updated successfully.')
        return redirect('user_list')

    messages.error(request, '❌ Invalid request method.')
    return redirect('user_list')


@has_model_permission('User', 'd')
def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.user.pk == user.pk:
        messages.error(request, "❌ You cannot delete your own account.")
        return redirect('user_list')

    if request.method == 'POST':
        user.delete()
        time = get_client_time(request)
        log_audit(request.user, 'delete', user,
                  details="User Deleted: '{}'".format(user.full_name),
                  new_data=safe_model_to_dict(user), request=request, timestamp=time)
        messages.success(request, '🗑️ User deleted successfully.')
        return redirect('user_list')

    messages.error(request, '❌ Invalid request method.')
    return redirect('user_list')
