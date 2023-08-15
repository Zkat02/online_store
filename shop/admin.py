from django.contrib import admin
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    list_display_links = ('user',)
    search_fields = ('user__username', 'phone_number', 'address')


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'seller_name', 'address')
    list_display_links = ('user',)
    search_fields = ('user__username', 'seller_name', 'address')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'seller')
    list_display_links = ('name', 'seller')
    list_filter = ('category',)
    search_fields = ('name', 'price', 'category__name', 'seller__seller_name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at',)
    list_display_links = ('customer',)
    search_fields = ('customer__user__username', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_display_links = ('cart',)
    search_fields = ('cart__customer__user__username', 'product__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price', 'created_at')
    list_display_links = ('customer',)
    search_fields = ('customer__user__username',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_display_links = ('order', 'product')
    search_fields = ('order__customer__user__username', 'product__name')
