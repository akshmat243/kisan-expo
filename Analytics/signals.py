from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timezone
from Analytics.models import (
    SalesAnalytics, CustomerAnalytics, CustomerLTVAnalytics, TopSellingProductAnalytics, CouponUsageAnalytics, InventoryAnalytics
)
from ECommerce.models import Order

@receiver(post_save, sender=Order)
def update_analytics_on_order(sender, instance, created, **kwargs):
    if not created or not instance.is_paid:
        return

    today = date.today()

    # --- SalesAnalytics ---
    analytics, _ = SalesAnalytics.objects.get_or_create(date=today)
    analytics.total_orders += 1
    analytics.total_paid_orders += 1
    analytics.total_sales += instance.total_amount
    analytics.avg_order_value = analytics.total_sales / analytics.total_paid_orders
    analytics.save()

    # --- CustomerAnalytics ---
    cust_analytics, _ = CustomerAnalytics.objects.get_or_create(user=instance.user)
    cust_analytics.total_orders += 1
    cust_analytics.total_spent += instance.total_amount
    cust_analytics.average_order_value = cust_analytics.total_spent / cust_analytics.total_orders
    cust_analytics.last_order_date = instance.ordered_at
    cust_analytics.is_repeat_customer = cust_analytics.total_orders > 1
    cust_analytics.save()

    # --- CustomerLTVAnalytics ---
    ltv, _ = CustomerLTVAnalytics.objects.get_or_create(user=instance.user)
    ltv.lifetime_value += instance.total_amount
    ltv.total_orders += 1
    ltv.last_order_date = instance.ordered_at
    if not ltv.first_order_date:
        ltv.first_order_date = instance.ordered_at
    ltv.save()

    # --- TopSellingProductAnalytics ---
    for item in instance.order_items.all():
        top, _ = TopSellingProductAnalytics.objects.get_or_create(product=item.product.id)
        top.total_units_sold += item.quantity
        top.total_revenue += item.price * item.quantity
        top.save()

@receiver(post_save, sender=Order)
def update_coupon_usage(sender, instance, created, **kwargs):
    if not created or not instance.is_paid or not instance.coupon:
        return

    coupon_code = instance.coupon.code
    discount_amount = instance.discount_amount

    obj, _ = CouponUsageAnalytics.objects.get_or_create(coupon_code=coupon_code)
    obj.times_used += 1
    obj.total_discount_given += discount_amount
    obj.last_used = instance.ordered_at
    obj.save()

@receiver(post_save, sender=Order)
def update_inventory_on_order(sender, instance, created, **kwargs):
    if not created or not instance.is_paid:
        return

    for item in instance.order_items.all():
        inv, _ = InventoryAnalytics.objects.get_or_create(product=item.product.id)
        inv.total_units_sold += item.quantity
        inv.current_stock = max(0, inv.current_stock - item.quantity)
        inv.is_low_stock = inv.current_stock < 10
        inv.save()

def update_inventory_on_restock(product_id, added_quantity):
    analytics, _ = InventoryAnalytics.objects.get_or_create(product=product_id)
    analytics.current_stock += added_quantity
    analytics.last_restocked = timezone.now()
    analytics.is_low_stock = analytics.current_stock < 10
    analytics.save()
