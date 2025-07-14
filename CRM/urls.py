from django.urls import path
from . import views

urlpatterns = [
    # Account URLs
    path('accounts/', views.account_list_view, name='account_list'),
    path('accounts/create/', views.account_create_view, name='account_create'),
    path('accounts/<uuid:pk>/edit/', views.account_edit_view, name='account_edit'),
    path('accounts/<uuid:pk>/delete/', views.account_delete_view, name='account_delete'),

    # Contact URLs
    path('contacts/', views.contact_list_view, name='contact_list'),
    path('contacts/create/', views.contact_create_view, name='contact_create'),
    path('contacts/<uuid:pk>/edit/', views.contact_edit_view, name='contact_edit'),
    path('contacts/<uuid:pk>/delete/', views.contact_delete_view, name='contact_delete'),

    # Lead URLs
    path('leads/', views.lead_list_view, name='lead_list'),
    path('leads/create/', views.lead_create_view, name='lead_create'),
    path('leads/<uuid:pk>/edit/', views.lead_edit_view, name='lead_edit'),
    path('leads/<uuid:pk>/delete/', views.lead_delete_view, name='lead_delete'),

    # Opportunity URLs
    path('opportunities/', views.opportunity_list_view, name='opportunity_list'),
    path('opportunities/create/', views.opportunity_create_view, name='opportunity_create'),
    path('opportunities/<uuid:pk>/edit/', views.opportunity_edit_view, name='opportunity_edit'),
    path('opportunities/<uuid:pk>/delete/', views.opportunity_delete_view, name='opportunity_delete'),

    # Activity URLs
    path('activities/', views.activity_list_view, name='activity_list'),
    path('activities/create/', views.activity_create_view, name='activity_create'),
    path('activities/<uuid:pk>/edit/', views.activity_edit_view, name='activity_edit'),
    path('activities/<uuid:pk>/delete/', views.activity_delete_view, name='activity_delete'),

    # OpportunityNote URLs
    path('opportunitynotes/', views.opportunitynote_list_view, name='opportunitynote_list'),
    path('opportunitynotes/create/', views.opportunitynote_create_view, name='opportunitynote_create'),
    path('opportunitynotes/<uuid:pk>/edit/', views.opportunitynote_edit_view, name='opportunitynote_edit'),
    path('opportunitynotes/<uuid:pk>/delete/', views.opportunitynote_delete_view, name='opportunitynote_delete'),

    # Document URLs
    path('documents/', views.document_list_view, name='document_list'),
    path('documents/create/', views.document_create_view, name='document_create'),
    path('documents/<uuid:pk>/edit/', views.document_edit_view, name='document_edit'),
    path('documents/<uuid:pk>/delete/', views.document_delete_view, name='document_delete'),
]
