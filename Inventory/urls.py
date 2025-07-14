from django.urls import path
from .views import *

urlpatterns = [
    path('warehouse/', warehouse_view, name="warehouse_list"),
    path('warehouse/create/', create_warehouse_view, name="warehouse_create"),
    path('warehouse/<uuid:pk>/edit/', edit_warehouse_view, name='warehouse_edit'),
    path('warehouse/<uuid:pk>/delete/', delete_warehouse_view, name='warehouse_delete'),

    path('inventory/', inventory_list_view, name='inventory_list'),
    path('inventory/create/', create_inventory_view, name='inventory_create'),
    path('inventory/<int:pk>/edit/', edit_inventory_view, name='inventory_edit'),
    path('inventory/<int:pk>/delete/', delete_inventory_view, name='inventory_delete'),
    
    path('stocktransactions/', stocktransaction_list_view, name='stocktransaction_list'),
    path('stocktransactions/create/', stocktransaction_create_view, name='stocktransaction_create'),
    path('stocktransactions/<uuid:pk>/edit/', stocktransaction_edit_view, name='stocktransaction_edit'),
    path('stocktransactions/<uuid:pk>/delete/', stocktransaction_delete_view, name='stocktransaction_delete'),
    
    path('stocktransfer/', stocktransfer_list_view, name='stocktransfer_list'),
    path('stocktransfer/create/', stocktransfer_create_view, name='stocktransfer_create'),
    path('stocktransfer/<uuid:pk>/edit/', stocktransfer_edit_view, name='stocktransfer_edit'),
    path('stocktransfer/<uuid:pk>/delete/', stocktransfer_delete_view, name='stocktransfer_delete'),
]
