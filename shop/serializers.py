from rest_framework import serializers
from .models import (
    Customer,
    # Category,
    Product,
    # Cart,
    # CartItem,
    # Order,
    # OrderItem,
    # Seller,
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
