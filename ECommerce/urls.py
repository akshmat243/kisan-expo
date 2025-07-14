from django.urls import path
from . import views

urlpatterns = [
    # Category
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/create/', views.category_create_view, name='category_create'),
    path('categories/<uuid:pk>/edit/', views.category_edit_view, name='category_edit'),
    path('categories/<uuid:pk>/delete/', views.category_delete_view, name='category_delete'),

    # Brand
    path('brands/', views.brand_list_view, name='brand_list'),
    path('brands/create/', views.brand_create_view, name='brand_create'),
    path('brands/<uuid:pk>/edit/', views.brand_edit_view, name='brand_edit'),
    path('brands/<uuid:pk>/delete/', views.brand_delete_view, name='brand_delete'),

    # Product
    path('products/', views.product_list_view, name='product_list'),
    path('products/create/', views.product_create_view, name='product_create'),
    path('products/<uuid:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<uuid:pk>/delete/', views.product_delete_view, name='product_delete'),

    # ProductImage
    path('product-images/', views.productimage_list_view, name='productimage_list'),
    path('product-images/create/', views.productimage_create_view, name='productimage_create'),
    path('product-images/<int:pk>/edit/', views.productimage_edit_view, name='productimage_edit'),
    path('product-images/<int:pk>/delete/', views.productimage_delete_view, name='productimage_delete'),

    # ProductReview
    path('reviews/', views.productreview_list_view, name='productreview_list'),
    path('reviews/create/', views.productreview_create_view, name='productreview_create'),
    path('reviews/<slug:slug>/<uuid:pk>/edit/', views.productreview_edit_view, name='productreview_edit'),
    path('reviews/<slug:slug>/<uuid:pk>/delete/', views.productreview_delete_view, name='productreview_delete'),

    # Cart
    path('carts/', views.cart_list_view, name='cart_list'),
    path('carts/create/', views.cart_create_view, name='cart_create'),
    path('carts/<uuid:pk>/edit/', views.cart_edit_view, name='cart_edit'),
    path('carts/<uuid:pk>/delete/', views.cart_delete_view, name='cart_delete'),

    # CartItem
    path('cart-items/', views.cartitem_list_view, name='cartitem_list'),
    path('cart-items/create/', views.cartitem_create_view, name='cartitem_create'),
    path('cart-items/<int:pk>/edit/', views.cartitem_edit_view, name='cartitem_edit'),
    path('cart-items/<int:pk>/delete/', views.cartitem_delete_view, name='cartitem_delete'),

    # Coupon
    path('coupons/', views.coupon_list_view, name='coupon_list'),
    path('coupons/create/', views.coupon_create_view, name='coupon_create'),
    path('coupons/<uuid:pk>/edit/', views.coupon_edit_view, name='coupon_edit'),
    path('coupons/<uuid:pk>/delete/', views.coupon_delete_view, name='coupon_delete'),

    # Order
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/create/', views.order_create_view, name='order_create'),
    path('orders/<uuid:pk>/edit/', views.order_edit_view, name='order_edit'),
    path('orders/<uuid:pk>/delete/', views.order_delete_view, name='order_delete'),

    # OrderItem
    path('order-items/', views.orderitem_list_view, name='orderitem_list'),
    path('order-items/create/', views.orderitem_create_view, name='orderitem_create'),
    path('order-items/<int:pk>/edit/', views.orderitem_edit_view, name='orderitem_edit'),
    path('order-items/<int:pk>/delete/', views.orderitem_delete_view, name='orderitem_delete'),

    # Payment
    path('payments/', views.payment_list_view, name='payment_list'),
    path('payments/create/', views.payment_create_view, name='payment_create'),
    path('payments/<uuid:pk>/edit/', views.payment_edit_view, name='payment_edit'),
    path('payments/<uuid:pk>/delete/', views.payment_delete_view, name='payment_delete'),
]
