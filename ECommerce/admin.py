from django.contrib import admin
from .models import (
    Category, Brand, Product, ProductImage, ProductReview,
    Cart, CartItem, Coupon, Order, OrderItem, Payment
)

### Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

### Brand Admin
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

### Product Image Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

### Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock', 'is_active')
    list_filter = ('category', 'brand', 'is_active')
    search_fields = ('name',)
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}

### Product Review Admin
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__full_name')

### Cart Item Inline
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    sfields = ('product', 'quantity')

### Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'created_at')
    inlines = [CartItemInline]
    search_fields = ('user__full_name',)

### Coupon Admin
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)

### Order Item Inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

### Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'is_paid', 'status', 'ordered_at')
    list_filter = ('status', 'is_paid', 'ordered_at')
    search_fields = ('user__full_name', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount',)

### Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_id', 'method', 'amount', 'payment_status', 'paid_at')
    list_filter = ('payment_status', 'method')
    search_fields = ('order__id', 'payment_id')
    readonly_fields = ('paid_at',)
