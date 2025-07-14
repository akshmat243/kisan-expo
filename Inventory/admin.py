from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from .models import Warehouse, Inventory, StockTransaction, StockTransfer

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'reorder_level')
    list_filter = ('warehouse', 'product')
    search_fields = ('product__name', 'warehouse__name')
    list_editable = ('quantity', 'reorder_level')


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'product', 'warehouse', 'quantity', 'created_by', 'created_at')
    list_filter = ('transaction_type', 'warehouse', 'created_at')
    search_fields = ('product__name', 'warehouse__name', 'note')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('product', 'warehouse', 'transaction_type', 'quantity')
        }),
        ('Additional Info', {
            'fields': ('note', 'created_by', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        try:
            super().save_model(request, obj, form, change)
        except ValueError as e:
            self.message_user(request, str(e), level=messages.ERROR)


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ('product', 'from_warehouse', 'to_warehouse', 'quantity', 'transferred_by', 'transferred_at')
    list_filter = ('from_warehouse', 'to_warehouse', 'transferred_at')
    search_fields = ('product__name', 'from_warehouse__name', 'to_warehouse__name')
    readonly_fields = ('transferred_at',)
    fieldsets = (
        (None, {
            'fields': ('product', 'from_warehouse', 'to_warehouse', 'quantity')
        }),
        ('Transfer Meta', {
            'fields': ('transferred_by', 'transferred_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.transferred_by:
            obj.transferred_by = request.user
        try:
            super().save_model(request, obj, form, change)
        except ValueError as e:
            self.message_user(request, str(e), level=messages.ERROR)
