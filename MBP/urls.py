from django.urls import path
from . import views

urlpatterns = [
    path('roles/', views.role_list_view, name='role_list'),
    path('roles/create/', views.create_role_view, name='create_role'),
    path('roles/<uuid:role_id>/edit/', views.role_edit_view, name='edit_role'),
    path('roles/<uuid:role_id>/delete/', views.role_delete_view, name='delete_role'),
    
    path('permission-types/', views.permission_type_list_view, name='permission_type_list'),
    path('permission-types/create/', views.create_permission_type_view, name='create_permission_type'),
    path('permission-types/<uuid:type_id>/edit/', views.permission_type_edit_view, name='edit_permission_type'),
    path('permission-types/<uuid:type_id>/delete/', views.delete_permission_type_view, name='delete_permission_type'),
    
    path('role-permissions/', views.get_role_permissions, name='get_role_permissions'),
    path('save-role-permissions/', views.save_role_permissions, name='save_role_permissions'),
    
    path('audit-logs/', views.audit_log_list_view, name='audit_log_list'),
    path('audit-logs/<int:log_id>/delete/', views.delete_auditlog_view, name='delete_log'),
]