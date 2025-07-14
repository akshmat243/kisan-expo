from django.shortcuts import render, get_object_or_404, redirect
from .models import Page
from django.utils.timezone import now
from .models import Page
from .forms import PageForm
from MBP.utils import log_audit, safe_model_to_dict
from MBP.views import get_client_time
from MBP.permission import has_model_permission
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone


def page_detail_view(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True, publish_date__lte=timezone.now())
    return render(request, f'CMS/pages/default.html', {'page': page})

@has_model_permission('Page', 'r')
def page_list_view(request):
    page_obj = Paginator(Page.objects.all().order_by('-created_at'), 10).get_page(request.GET.get('page'))
    return render(request, "CMS/pages/list.html", {"page_obj": page_obj})


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