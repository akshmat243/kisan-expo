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
from .views import (
    Section_list_view, Section_create_view, Section_edit_view, Section_delete_view,
    Image_list_view, Image_create_view, Image_edit_view, Image_delete_view,
    Video_list_view, Video_create_view, Video_edit_view, Video_delete_view,
    FAQ_list_view, FAQ_create_view, FAQ_edit_view, FAQ_delete_view,
    Banner_list_view, Banner_create_view, Banner_edit_view, Banner_delete_view,
    Testimonial_list_view, Testimonial_create_view, Testimonial_edit_view, Testimonial_delete_view,
    MetaTag_list_view, MetaTag_create_view, MetaTag_edit_view, MetaTag_delete_view,
)

urlpatterns += [
    # Section URLs
    path('sections/', Section_list_view, name='section_list'),
    path('sections/create/', Section_create_view, name='section_create'),
    path('sections/<int:pk>/edit/', Section_edit_view, name='section_edit'),
    path('sections/<int:pk>/delete/', Section_delete_view, name='section_delete'),

    # Image URLs
    path('images/', Image_list_view, name='image_list'),
    path('images/create/', Image_create_view, name='image_create'),
    path('images/<int:pk>/edit/', Image_edit_view, name='image_edit'),
    path('images/<int:pk>/delete/', Image_delete_view, name='image_delete'),

    # Video URLs
    path('videos/', Video_list_view, name='video_list'),
    path('videos/create/', Video_create_view, name='video_create'),
    path('videos/<int:pk>/edit/', Video_edit_view, name='video_edit'),
    path('videos/<int:pk>/delete/', Video_delete_view, name='video_delete'),

    # FAQ URLs
    path('faqs/', FAQ_list_view, name='faq_list'),
    path('faqs/create/', FAQ_create_view, name='faq_create'),
    path('faqs/<int:pk>/edit/', FAQ_edit_view, name='faq_edit'),
    path('faqs/<int:pk>/delete/', FAQ_delete_view, name='faq_delete'),

    # Banner URLs
    path('banners/', Banner_list_view, name='banner_list'),
    path('banners/create/', Banner_create_view, name='banner_create'),
    path('banners/<int:pk>/edit/', Banner_edit_view, name='banner_edit'),
    path('banners/<int:pk>/delete/', Banner_delete_view, name='banner_delete'),

    # Testimonial URLs
    path('testimonials/', Testimonial_list_view, name='testimonial_list'),
    path('testimonials/create/', Testimonial_create_view, name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', Testimonial_edit_view, name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', Testimonial_delete_view, name='testimonial_delete'),

    # MetaTag URLs
    path('metatags/', MetaTag_list_view, name='metatag_list'),
    path('metatags/create/', MetaTag_create_view, name='metatag_create'),
    path('metatags/<int:pk>/edit/', MetaTag_edit_view, name='metatag_edit'),
    path('metatags/<int:pk>/delete/', MetaTag_delete_view, name='metatag_delete'),
]
