from rest_framework import serializers
from .models import (
    Customer,
    Category,
    Product,
    User,
    # Cart,
    # CartItem,
    # Order,
    # OrderItem,
    Seller,
)
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('seller_name', 'address')


class UserSellerSerializer(serializers.HyperlinkedModelSerializer):
    seller = SellerSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'seller')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        seller_data = validated_data.pop('seller')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Seller.objects.create(user=user, **seller_data)
        return user


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('phone_number', 'address')


class UserCustomerSerializer(serializers.HyperlinkedModelSerializer):
    customer = CustomerSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'customer')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Customer.objects.create(user=user, **customer_data)
        return user

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer')
        customer = instance.customer

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        customer.address = profile_data.get('address', customer.address)
        customer.phone_number = profile_data.get('phone_number', customer.phone_number)
        customer.save()

        return instance


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
