from django.contrib import admin
from .models import (
    SalesAnalytics, ProductAnalytics, CustomerAnalytics,
    CouponUsageAnalytics, InventoryAnalytics, TrafficSourceAnalytics,
    TrafficLog, CustomerLTVAnalytics, TopSellingProductAnalytics,
    ProductViewLog
)

@admin.register(SalesAnalytics)
class SalesAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_orders', 'total_sales', 'avg_order_value', 'total_paid_orders', 'total_canceled_orders']
    list_filter = ['date']
    ordering = ['-date']


@admin.register(ProductAnalytics)
class ProductAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'total_views', 'total_purchases', 'average_rating', 'last_updated']
    search_fields = ['product']
    ordering = ['-last_updated']


@admin.register(CustomerAnalytics)
class CustomerAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_orders', 'total_spent', 'average_order_value', 'last_order_date', 'is_repeat_customer']
    list_filter = ['is_repeat_customer']
    search_fields = ['user__username', 'user__email']
    ordering = ['-last_order_date']


@admin.register(CouponUsageAnalytics)
class CouponUsageAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'times_used', 'total_discount_given', 'last_used']
    search_fields = ['coupon_code']
    ordering = ['-last_used']


@admin.register(InventoryAnalytics)
class InventoryAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['product', 'current_stock', 'total_units_sold', 'last_restocked', 'is_low_stock']
    list_filter = ['is_low_stock']
    ordering = ['-last_restocked']


@admin.register(TrafficSourceAnalytics)
class TrafficSourceAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['source', 'visits', 'conversions', 'bounce_rate']
    search_fields = ['source']
    ordering = ['-visits']


@admin.register(TrafficLog)
class TrafficLogAdmin(admin.ModelAdmin):
    list_display = ['source', 'user', 'session_id', 'converted', 'visited_at']
    list_filter = ['converted', 'source']
    search_fields = ['source', 'user__username', 'session_id']
    ordering = ['-visited_at']


@admin.register(CustomerLTVAnalytics)
class CustomerLTVAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'lifetime_value', 'total_orders', 'first_order_date', 'last_order_date', 'is_active_customer']
    list_filter = ['is_active_customer']
    search_fields = ['user__username', 'user__email']
    ordering = ['-lifetime_value']


@admin.register(TopSellingProductAnalytics)
class TopSellingProductAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['product', 'total_units_sold', 'total_revenue']
    ordering = ['-total_units_sold']


@admin.register(ProductViewLog)
class ProductViewLogAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'ip_address', 'session_key', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['product', 'user__username', 'ip_address', 'session_key']
    ordering = ['-viewed_at']
