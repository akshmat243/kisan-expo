from django.urls import path
from .views import (
    register_view, login_view, dashboard_view, logout_view,
    user_create_view, user_delete_view, user_edit_view, user_list_view,
    get_notifications, delete_notification,
    profile_view, change_password
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    path('users/', user_list_view, name='user_list'),
    path('users/create/', user_create_view, name='create_user'),
    path('users/<uuid:pk>/edit/', user_edit_view, name='edit_user'),
    path('users/<uuid:pk>/delete/', user_delete_view, name='delete_user'),
    path('change-password/', change_password, name='change_password'),
    
    path('get-notifications/', get_notifications, name='get_notifications'),
    path('notifications/delete/<int:pk>/', delete_notification, name='delete_notification'),

    path('profile/', profile_view, name='profile'),

]
