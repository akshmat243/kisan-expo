import uuid
from django.db import models
from django.utils.timezone import now
from ECommerce.models import Product
from accounts.models import User

class SalesAnalytics(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid_orders = models.PositiveIntegerField(default=0)
    total_canceled_orders = models.PositiveIntegerField(default=0)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Sales on {self.date}"


class ProductAnalytics(models.Model):
    product = models.UUIDField()
    total_views = models.PositiveIntegerField(default=0)
    total_purchases = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for Product {self.product}"
    
    def product_name(self):
        try:
            return Product.objects.get(id=self.product).name
        except Product.DoesNotExist:
            return "Unknown"
    product_name.short_description = "Product Name"


class CustomerAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_order_date = models.DateTimeField(null=True, blank=True)
    is_repeat_customer = models.BooleanField(default=False)

    def __str__(self):
        return f"Analytics for {self.user.username}"
    

class CouponUsageAnalytics(models.Model):
    coupon_code = models.CharField(max_length=20)
    times_used = models.PositiveIntegerField(default=0)
    total_discount_given = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.coupon_code} - Used {self.times_used} times"


class InventoryAnalytics(models.Model):
    product = models.UUIDField()
    current_stock = models.PositiveIntegerField(default=0)
    total_units_sold = models.PositiveIntegerField(default=0)
    last_restocked = models.DateTimeField(null=True, blank=True)
    is_low_stock = models.BooleanField(default=False)

    def __str__(self):
        return f"Inventory for Product {self.product}"


class TrafficSourceAnalytics(models.Model):
    source = models.CharField(max_length=255)  # e.g., Google, Facebook
    visits = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    bounce_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.source} - Visits: {self.visits}"

class TrafficLog(models.Model):
    source = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.CharField(max_length=64)
    converted = models.BooleanField(default=False)
    visited_at = models.DateTimeField(auto_now_add=True)

class CustomerLTVAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    first_order_date = models.DateTimeField(null=True, blank=True)
    last_order_date = models.DateTimeField(null=True, blank=True)
    total_orders = models.PositiveIntegerField(default=0)
    is_active_customer = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - LTV: ₹{self.lifetime_value}"


class TopSellingProductAnalytics(models.Model):
    product = models.UUIDField()
    total_units_sold = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Top Selling Product {self.product} - {self.total_units_sold} units"

class ProductViewLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.UUIDField()  # Reference to Product's UUID
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(default=now)

    class Meta:
        indexes = [
            models.Index(fields=['product', 'viewed_at']),
        ]
        ordering = ['-viewed_at']

    def __str__(self):
        return f"View: {self.product} by {self.user or self.ip_address} at {self.viewed_at}"