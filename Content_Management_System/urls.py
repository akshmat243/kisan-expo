from django.urls import path
from . import views

urlpatterns = [
    path("pages/", views.page_list_view, name="page_list"),
    path("pages/create/", views.page_create_view, name="page_create"),
    path("pages/<uuid:pk>/edit/", views.page_edit_view, name="page_edit"),
    path("pages/<uuid:pk>/delete/", views.page_delete_view, name="page_delete"),

    # Public live page view via slug
    path("pages/<slug:slug>/", views.page_detail_view, name="page_view"),
]
