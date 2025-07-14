import uuid
from django.db import models, transaction
from ECommerce.models import Product
from accounts.models import User

class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'warehouse')

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name} ({self.quantity})"


class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Stock Adjustment'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField(help_text="Quantity of stock")
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            inventory, _ = Inventory.objects.get_or_create(
                product=self.product,
                warehouse=self.warehouse,
                defaults={'quantity': 0}
            )

            if self.pk:
                old = StockTransaction.objects.get(pk=self.pk)
                if old.transaction_type == 'in':
                    inventory.quantity -= old.quantity
                elif old.transaction_type == 'out':
                    inventory.quantity += old.quantity
                elif old.transaction_type == 'adjust':
                    pass

            if self.transaction_type == 'in':
                inventory.quantity += self.quantity
            elif self.transaction_type == 'out':
                if inventory.quantity < self.quantity:
                    raise ValueError("Not enough stock to complete this transaction.")
                inventory.quantity -= self.quantity
            elif self.transaction_type == 'adjust':
                inventory.quantity = self.quantity

            inventory.save()
            super().save(*args, **kwargs)


class StockTransfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_warehouse = models.ForeignKey(Warehouse, related_name='transfers_out', on_delete=models.CASCADE)
    to_warehouse = models.ForeignKey(Warehouse, related_name='transfers_in', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    transferred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transferred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} from {self.from_warehouse} to {self.to_warehouse}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            from_inventory, _ = Inventory.objects.get_or_create(
                product=self.product,
                warehouse=self.from_warehouse,
                defaults={'quantity': 0}
            )

            if from_inventory.quantity < self.quantity:
                raise ValueError("Not enough stock to transfer.")

            to_inventory, _ = Inventory.objects.get_or_create(
                product=self.product,
                warehouse=self.to_warehouse,
                defaults={'quantity': 0}
            )

            from_inventory.quantity -= self.quantity
            to_inventory.quantity += self.quantity

            from_inventory.save()
            to_inventory.save()
            super().save(*args, **kwargs)

