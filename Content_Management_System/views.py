from django.shortcuts import render, get_object_or_404, redirect
from .models import Page
from .models import Page, Section, Image, Video, FAQ, Banner, Testimonial, MetaTag
from .forms import PageForm, SectionForm, ImageForm, VideoForm, FAQForm, BannerForm, TestimonialForm, MetaTagForm
from MBP.utils import log_audit, safe_model_to_dict
from MBP.views import get_client_time
from MBP.permission import has_model_permission
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify
from MBP.utils import dev_time_now

def page_detail_view(request, slug):
    try:
        page = Page.objects.get(slug=slug)
        if not page.is_published or (page.publish_date and page.publish_date > dev_time_now()):
            return render(request, "CMS/pages/default.html", {
                "error_message": "🚫 This page is not published yet.",
                "page": page
            })
        return render(request, f"CMS/pages/{page.template}", {"page": page})
    except Page.DoesNotExist:
        return render(request, "CMS/pages/default.html", {
            "error_message": "❌ Page not found."
        })

@has_model_permission('Page', 'r')
def page_list_view(request):
    protected_slug =['home', '404-page']
    page_obj = Paginator(Page.objects.all().order_by('created_at'), 10).get_page(request.GET.get('page'))
    return render(request, "CMS/pages/list.html", {"page_obj": page_obj, "protected_slugs": protected_slug})


@has_model_permission('Page', 'c')
def page_create_view(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.slug = slugify(page.title)
            page.save()
            log_audit(
                user=request.user,
                action='create',
                instance=page,
                details="Page Created",
                new_data=safe_model_to_dict(page),
                request=request,
                timestamp=get_client_time(request)
            )
            messages.success(request, "✅ Page created successfully.")
            return redirect("page_list")
    else:
        form = PageForm()
    return render(request, "CMS/pages/form.html", {"form": form})


@has_model_permission('Page', 'u')
def page_edit_view(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        old_data = safe_model_to_dict(page)
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            updated_page = form.save(commit=False)
            updated_page.slug = slugify(updated_page.title)
            updated_page.save()
            log_audit(
                user=request.user,
                action='update',
                instance=updated_page,
                details="Page Updated",
                old_data=old_data,
                new_data=safe_model_to_dict(updated_page),
                request=request,
                timestamp=get_client_time(request)
            )
            messages.success(request, "✅ Page updated successfully.")
            return redirect("page_list")
    else:
        form = PageForm(instance=page)
    return render(request, "CMS/pages/form.html", {"form": form})


@has_model_permission('Page', 'd')
def page_delete_view(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        old_data = safe_model_to_dict(page)
        page.delete()
        log_audit(
            user=request.user,
            action='delete',
            instance=page,
            details="Page Deleted",
            new_data=old_data,
            request=request,
            timestamp=get_client_time(request)
        )
        messages.success(request, "🗑️ Page deleted successfully.")
        return redirect("page_list")
    
    messages.error(request, "❌ Invalid request method.")
    return redirect('page_list')



# Generic CRUD views generator
def generate_crud_views(model, form_class, model_name):
    @has_model_permission(model_name, 'r')
    def list_view(request):
        objects = model.objects.all().order_by('-pk')
        paginator = Paginator(objects, 10)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, f'CMS/{model_name.lower()}/list.html', {'page_obj': page_obj})

    @has_model_permission(model_name, 'c')
    def create_view(request):
        form = form_class(request.POST or None, request.FILES or None)
        if request.method == 'POST' and form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            log_audit(
                user=request.user,
                action='create',
                instance=instance,
                details=f"{model_name} Created",
                new_data=safe_model_to_dict(instance),
                request=request,
                timestamp=get_client_time(request)
            )
            messages.success(request, f"✅ {model_name} created successfully.")
            return redirect(f'{model_name.lower()}_list')
        return render(request, f'CMS/{model_name.lower()}/form.html', {'form': form})

    @has_model_permission(model_name, 'u')
    def edit_view(request, pk):
        instance = get_object_or_404(model, pk=pk)
        old_data = safe_model_to_dict(instance)
        form = form_class(request.POST or None, request.FILES or None, instance=instance)
        if request.method == 'POST' and form.is_valid():
            instance = form.save()
            log_audit(
                user=request.user,
                action='update',
                instance=instance,
                details=f"{model_name} Updated",
                old_data=old_data,
                new_data=safe_model_to_dict(instance),
                request=request,
                timestamp=get_client_time(request)
            )
            messages.success(request, f"✅ {model_name} updated successfully.")
            return redirect(f'{model_name.lower()}_list')
        return render(request, f'CMS/{model_name.lower()}/form.html', {'form': form})

    @has_model_permission(model_name, 'd')
    def delete_view(request, pk):
        if request.method == 'POST':
            instance = get_object_or_404(model, pk=pk)
            old_data = safe_model_to_dict(instance)
            instance.delete()
            log_audit(
                user=request.user,
                action='delete',
                instance=instance,
                details=f"{model_name} Deleted",
                new_data=old_data,
                request=request,
                timestamp=get_client_time(request)
            )
            messages.success(request, f"🗑️ {model_name} deleted successfully.")
            return redirect(f'{model_name.lower()}_list')

        messages.error(request, "❌ Invalid request method.")
        return redirect(f'{model_name.lower()}_list')

    return list_view, create_view, edit_view, delete_view

# Registering all models and their views
Section_list_view, Section_create_view, Section_edit_view, Section_delete_view = generate_crud_views(Section, SectionForm, 'Section')
Image_list_view, Image_create_view, Image_edit_view, Image_delete_view = generate_crud_views(Image, ImageForm, 'Image')
Video_list_view, Video_create_view, Video_edit_view, Video_delete_view = generate_crud_views(Video, VideoForm, 'Video')
FAQ_list_view, FAQ_create_view, FAQ_edit_view, FAQ_delete_view = generate_crud_views(FAQ, FAQForm, 'FAQ')
Banner_list_view, Banner_create_view, Banner_edit_view, Banner_delete_view = generate_crud_views(Banner, BannerForm, 'Banner')
Testimonial_list_view, Testimonial_create_view, Testimonial_edit_view, Testimonial_delete_view = generate_crud_views(Testimonial, TestimonialForm, 'Testimonial')
MetaTag_list_view, MetaTag_create_view, MetaTag_edit_view, MetaTag_delete_view = generate_crud_views(MetaTag, MetaTagForm, 'MetaTag')
