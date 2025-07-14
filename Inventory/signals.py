# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import StockTransaction, Inventory, StockTransfer

# @receiver(post_save, sender=StockTransaction)
# def update_inventory_on_transaction(sender, instance, created, **kwargs):
#     if created:
#         inventory, _ = Inventory.objects.get_or_create(
#             product=instance.product,
#             warehouse=instance.warehouse,
#             defaults={'quantity': 0}
#         )
#         inventory.quantity += instance.quantity
#         inventory.save()

# @receiver(post_save, sender=StockTransfer)
# def update_inventory_on_transfer(sender, instance, created, **kwargs):
#     if created:
#         from_inventory, _ = Inventory.objects.get_or_create(
#             product=instance.product,
#             warehouse=instance.from_warehouse,
#             defaults={'quantity': 0}
#         )
#         from_inventory.quantity -= instance.quantity
#         from_inventory.save()

#         to_inventory, _ = Inventory.objects.get_or_create(
#             product=instance.product,
#             warehouse=instance.to_warehouse,
#             defaults={'quantity': 0}
#         )
#         to_inventory.quantity += instance.quantity
#         to_inventory.save()
