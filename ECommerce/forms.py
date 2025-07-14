from django import forms
from .models import (
    Category, Brand, Product, ProductImage, ProductReview,
    Cart, CartItem, Coupon, Order, OrderItem, Payment
)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'brand', 'description',
            'price', 'discount_price', 'stock', 'is_active'
        ]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'is_feature']

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['product', 'user', 'rating', 'comment']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'total_amount']

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percent', 'valid_from', 'valid_to', 'is_active']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user', 'cart', 'coupon', 'status', 'total_amount',
            'shipping_address', 'billing_address', 'payment_method', 'is_paid'
        ]

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'payment_id', 'method', 'amount', 'payment_status']
