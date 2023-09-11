from rest_framework import serializers
from .models import (
    Customer,
    Category,
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    # Nested Serializers
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price can not be negative")
        return value
