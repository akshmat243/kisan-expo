from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem, Order, OrderItem, Payment

@receiver([post_save, post_delete], sender=CartItem)
def sync_order_with_cart(sender, instance, **kwargs):
    cart = instance.cart
    user = cart.user

    # Recalculate cart total
    total = 0
    for item in cart.items.all():
        total += item.product.price * item.quantity

    cart.total_amount = total
    cart.save()

    # Create or update order
    order, created = Order.objects.get_or_create(
        cart=cart,
        defaults={
            'user': user,
            'total_amount': total,
            'shipping_address': 'TBD',
            'billing_address': 'TBD',
            'payment_method': 'TBD',
            'is_paid': False,
        }
    )

    # Always update order total
    order.total_amount = total
    order.save()

    # Sync OrderItems
    order.order_items.all().delete()
    for item in cart.items.all():
        if item.product and item.product.price is not None:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )


    # ✅ Fix here: explicitly set `amount` while creating Payment
    payment, created = Payment.objects.get_or_create(order=order, defaults={
        'payment_id': 'TEMP',  # You can set a placeholder until real payment happens
        'method': 'admin',     # or 'cash on delivery' or 'N/A'
        'amount': total,
    })

    # If payment already exists, update its amount
    if not created:
        payment.amount = total
        payment.save()
