from .models import *
from .forms import *
from MBP.permission import has_model_permission
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from MBP.views import get_client_time
from MBP.utils import log_audit, safe_model_to_dict
from django.contrib import messages



MODEL_VIEW_CONFIG = [
    (Category, CategoryForm, 'category'),
    (Brand, BrandForm, 'brand'),
    (Product, ProductForm, 'product'),
    (ProductImage, ProductImageForm, 'productimage'),
    (ProductReview, ProductReviewForm, 'productreview'),
    (Cart, CartForm, 'cart'),
    (CartItem, CartItemForm, 'cartitem'),
    (Coupon, CouponForm, 'coupon'),
    (Order, OrderForm, 'order'),
    (OrderItem, OrderItemForm, 'orderitem'),
    (Payment, PaymentForm, 'payment'),
]

for model, form_class, model_name in MODEL_VIEW_CONFIG:
    globals()[f"{model_name}_list_view"] = has_model_permission(model.__name__, 'r')(
        lambda request, model=model, model_name=model_name: render(
            request, f"Ecommerce/{model_name}/list.html",
            {
                'page_obj': Paginator(model.objects.all(), 10).get_page(
                    request.GET.get("page")
                )
            }
        )
    )

    def create_view(request, model=model, form_class=form_class, model_name=model_name):
        if request.method == 'POST':
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save()
                log_audit(
                    request.user, 'create', instance,
                    details=f"{model.__name__} Created",
                    new_data=safe_model_to_dict(instance),
                    request=request,
                    timestamp=get_client_time(request)
                )
                messages.success(request, f"✅ {model.__name__} created successfully.")
                return redirect(f"{model_name}_list")
        else:
            form = form_class()
        return render(request, f"Ecommerce/{model_name}/form.html", {'form': form})

    globals()[f"{model_name}_create_view"] = has_model_permission(model.__name__, 'c')(create_view)

    def edit_view(request, slug=None, pk=None, model=model, form_class=form_class, model_name=model_name):
        instance = get_object_or_404(model, pk=pk)
        if request.method == 'POST':
            old_data = safe_model_to_dict(instance)
            form = form_class(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                updated = form.save()
                log_audit(request.user, 'update', updated,
                    details=f"{model.__name__} Updated",
                    old_data=old_data, new_data=safe_model_to_dict(updated),
                    request=request, timestamp=get_client_time(request))
                messages.success(request, f"✅ {model.__name__} updated successfully.")
                return redirect(f"{model_name}_list")
        else:
            form = form_class(instance=instance)
        return render(request, f"Ecommerce/{model_name}/form.html", {'form': form})

    globals()[f"{model_name}_edit_view"] = has_model_permission(model.__name__, 'u')(edit_view)

    def delete_view(request, slug=None, pk=None, model=model, model_name=model_name):
        instance = get_object_or_404(model, pk=pk)
        if request.method == 'POST':
            old_data = safe_model_to_dict(instance)
            instance.delete()
            log_audit(request.user, 'delete', instance,
                details=f"{model.__name__} Deleted",
                new_data=old_data, request=request, timestamp=get_client_time(request))
            messages.success(request, f"🗑️ {model.__name__} deleted successfully.")
        return redirect(f"{model_name}_list")

    globals()[f"{model_name}_delete_view"] = has_model_permission(model.__name__, 'd')(delete_view)
