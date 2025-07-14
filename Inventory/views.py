from django.shortcuts import render, redirect, get_object_or_404
from .models import Warehouse, Inventory, StockTransaction, StockTransfer
from .forms import StockTransactionForm, StockTransferForm
from ECommerce.models import Product
from MBP.permission import has_model_permission
from MBP.utils import log_audit, model_to_dict, safe_model_to_dict
from MBP.views import get_client_time
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator



@has_model_permission('Warehouse', 'r')
def warehouse_view(request):
    search = request.GET.get('search', '')
    warehouses = Warehouse.objects.all().order_by('name')
    
    if search:
        warehouses = warehouses.filter(name__icontains=search)
    
    return render(request, 'inventory/warehouse.html', {
        'warehouses': warehouses,
        'search': search,
    })

@has_model_permission('Warehouse', 'c')
def create_warehouse_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        location = request.POST.get('location', '').strip()

        if not name:
            messages.error(request, "⚠️ Warehouse name is required.")
            return redirect('warehouse_list')

        if Warehouse.objects.filter(name=name).exists():
            messages.error(request, "⚠️ Warehouse with this name already exists.")
        else:
            new_warehouse = Warehouse.objects.create(name=name, location=location)
            time = get_client_time(request)
            log_audit(
                request.user, 'create', new_warehouse,
                details=f"New Warehouse Created: '{name}'",
                new_data=model_to_dict(new_warehouse),
                request=request,
                timestamp=time
            )
            messages.success(request, "✅ Warehouse created successfully.")
    return redirect('warehouse_list')

@has_model_permission('Warehouse', 'u')
def edit_warehouse_view(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        location = request.POST.get('location', '').strip()

        if not name:
            messages.error(request, "⚠️ Warehouse name is required.")
            return redirect('warehouse_list')

        if Warehouse.objects.exclude(id=pk).filter(name=name).exists():
            messages.error(request, "⚠️ Another warehouse with this name already exists.")
            return redirect('warehouse_list')

        old_data = model_to_dict(warehouse)
        warehouse.name = name
        warehouse.location = location
        warehouse.save()

        time = get_client_time(request)
        log_audit(
            request.user,
            action='update',
            instance=warehouse,
            details=f"Updated Warehouse: '{name}'",
            old_data=old_data,
            new_data=model_to_dict(warehouse),
            request=request,
            timestamp=time
        )

        messages.success(request, "✅ Warehouse updated successfully.")
        return redirect('warehouse_list')
    
@has_model_permission('Warehouse', 'd')
def delete_warehouse_view(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)

    if request.method == 'POST':
        time = get_client_time(request)
        old_data = model_to_dict(warehouse)
        warehouse_name = warehouse.name

        warehouse.delete()

        log_audit(
            user=request.user,
            action='delete',
            instance=warehouse,
            details=f"Deleted Warehouse: '{warehouse_name}'",
            old_data=old_data,
            request=request,
            timestamp=time
        )

        messages.success(request, "🗑️ Warehouse deleted successfully.")
    else:
        messages.error(request, "❌ Invalid request method.")

    return redirect('warehouse_list')

@has_model_permission('Inventory', 'r')
def inventory_list_view(request):
    search = request.GET.get('search', '').strip()
    
    inventories = Inventory.objects.all()
    products = Product.objects.all()
    warehouses = Warehouse.objects.all()

    if search:
        inventories = inventories.filter(
            Q(product__name__icontains=search) |
            Q(warehouse__name__icontains=search)
        )

    paginator = Paginator(inventories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'inventories' :page_obj.object_list,
        'page_obj': page_obj,
        'search': search,
        'products' : products,
        'warehouses' : warehouses
    }
    return render(request, 'inventory/inventory.html', context)

@has_model_permission('Inventory', 'c')
def create_inventory_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        warehouse_id = request.POST.get('warehouse')
        quantity = request.POST.get('quantity', 0)
        reorder_level = request.POST.get('reorder_level', 0)

        try:
            product = Product.objects.get(id=product_id)
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except (Product.DoesNotExist, Warehouse.DoesNotExist):
            messages.error(request, "❌ Invalid product or warehouse.")
            return redirect('inventory_list')

        if Inventory.objects.filter(product=product, warehouse=warehouse).exists():
            messages.error(request, "⚠️ Inventory entry already exists for this product in this warehouse.")
            return redirect('inventory_list')

        inventory = Inventory.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=quantity,
            reorder_level=reorder_level
        )

        inventory_dict = model_to_dict(inventory)
        inventory_dict['product'] = str(product.id)
        inventory_dict['warehouse'] = str(warehouse.id)

        log_audit(
            user=request.user,
            action='create',
            instance=inventory,
            details=f"Created Inventory for {product.name} in {warehouse.name}",
            new_data=inventory_dict,
            request=request,
            timestamp=get_client_time(request)
        )

        messages.success(request, "✅ Inventory added successfully.")

    return redirect('inventory_list')

@has_model_permission('Inventory', 'u')
def edit_inventory_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        product_id = request.POST.get('product')
        warehouse_id = request.POST.get('warehouse')
        quantity = request.POST.get('quantity', 0)
        reorder_level = request.POST.get('reorder_level', 0)

        try:
            product = Product.objects.get(id=product_id)
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except (Product.DoesNotExist, Warehouse.DoesNotExist):
            messages.error(request, "❌ Invalid product or warehouse.")
            return redirect('inventory_list')

        if Inventory.objects.exclude(id=inventory.id).filter(product=product, warehouse=warehouse).exists():
            messages.error(request, "⚠️ Inventory with this product and warehouse already exists.")
            return redirect('inventory_list')

        old_data = {
            "product": str(inventory.product),
            "warehouse": str(inventory.warehouse),
            "quantity": inventory.quantity,
            "reorder_level": inventory.reorder_level,
        }

        inventory.product = product
        inventory.warehouse = warehouse
        inventory.quantity = quantity
        inventory.reorder_level = reorder_level
        inventory.save()

        new_data = {
            "product": str(inventory.product),
            "warehouse": str(inventory.warehouse),
            "quantity": inventory.quantity,
            "reorder_level": inventory.reorder_level,
        }

        log_audit(
            request.user, 'update', inventory,
            details=f"Updated Inventory for {product.name} in {warehouse.name}",
            old_data=old_data,
            new_data=new_data,
            request=request,
            timestamp=get_client_time(request)
        )

        messages.success(request, "✅ Inventory updated successfully.")
    return redirect('inventory_list')

@has_model_permission('Inventory', 'd')
def delete_inventory_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == 'POST':
        old_data = safe_model_to_dict(inventory)
        product_name = inventory.product.name
        warehouse_name = inventory.warehouse.name
        time = get_client_time(request)
        print(product_name, warehouse_name)
        inventory.delete()

        log_audit(
            request.user,
            action='delete',
            instance=inventory,
            details=f"Inventory Deleted: Product '{product_name}' from Warehouse '{warehouse_name}'",
            old_data=old_data,
            request=request,
            timestamp=time,
        )

        messages.success(request, "🗑️ Inventory entry deleted successfully.")
        return redirect('inventory_list')

    messages.error(request, "❌ Invalid request method.")
    return redirect('inventory_list')


@has_model_permission('StockTransaction', 'r')
def stocktransaction_list_view(request):
    page_obj = Paginator(StockTransaction.objects.select_related('product', 'warehouse', 'created_by'), 10).get_page(request.GET.get('page'))
    return render(request, "inventory/stocktransaction/list.html", {"page_obj": page_obj})

@has_model_permission('StockTransaction', 'c')
def stocktransaction_create_view(request):
    if request.method == "POST":
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            transaction_instance = form.save(commit=False)
            transaction_instance.created_by = request.user
            transaction_instance.save()
            log_audit(request.user, 'create', transaction_instance, details="StockTransaction Created", new_data=safe_model_to_dict(transaction_instance), request=request, timestamp=get_client_time(request))
            messages.success(request, "✅ StockTransaction created successfully.")
            return redirect("stocktransaction_list")
    else:
        form = StockTransactionForm()
    return render(request, "inventory/stocktransaction/form.html", {"form": form})

@has_model_permission('StockTransaction', 'u')
def stocktransaction_edit_view(request, pk):
    instance = get_object_or_404(StockTransaction, pk=pk)
    if request.method == "POST":
        old_data = safe_model_to_dict(instance)
        form = StockTransactionForm(request.POST, instance=instance)
        if form.is_valid():
            updated_instance = form.save()
            log_audit(request.user, 'update', updated_instance, details="StockTransaction Updated", old_data=old_data, new_data=safe_model_to_dict(updated_instance), request=request, timestamp=get_client_time(request))
            messages.success(request, "✅ StockTransaction updated successfully.")
            return redirect("stocktransaction_list")
    else:
        form = StockTransactionForm(instance=instance)
    return render(request, "inventory/stocktransaction/form.html", {"form": form})

@has_model_permission('StockTransaction', 'd')
def stocktransaction_delete_view(request, pk):
    instance = get_object_or_404(StockTransaction, pk=pk)
    if request.method == "POST":
        old_data = safe_model_to_dict(instance)
        instance.delete()
        log_audit(request.user, 'delete', instance, details="StockTransaction Deleted", new_data=old_data, request=request, timestamp=get_client_time(request))
        messages.success(request, "🗑️ StockTransaction deleted successfully.")
        return redirect("stocktransaction_list")


@has_model_permission('StockTransfer', 'r')
def stocktransfer_list_view(request):
    transfers = StockTransfer.objects.select_related('product', 'from_warehouse', 'to_warehouse')
    paginator = Paginator(transfers, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'inventory/stocktransfer/list.html', {
        'page_obj': page_obj
    })


@has_model_permission('StockTransfer', 'c')
def stocktransfer_create_view(request):
    form = StockTransferForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        transfer = form.save(commit=False)
        transfer.transferred_by = request.user
        transfer.save()
        return redirect('stocktransfer_list')
    return render(request, 'inventory/stocktransfer/form.html', {
        'form': form
    })


@has_model_permission('StockTransfer', 'u')
def stocktransfer_edit_view(request, pk):
    transfer = get_object_or_404(StockTransfer, pk=pk)
    form = StockTransferForm(request.POST or None, instance=transfer)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('stocktransfer_list')
    return render(request, 'inventory/stocktransfer/form.html', {
        'form': form
    })


@has_model_permission('StockTransfer', 'd')
def stocktransfer_delete_view(request, pk):
    transfer = get_object_or_404(StockTransfer, pk=pk)
    if request.method == 'POST':
        transfer.delete()
        return redirect('stocktransfer_list')
    return render(request, 'partials/confirm_delete.html', {
        'object': transfer,
        'cancel_url': 'stocktransfer_list'
    })