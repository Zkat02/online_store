from django.test import TestCase
from shop.models import Category, Seller, Product
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CategoryModelTest(TestCase):
    def test_str_representation(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")


class SellerModelTest(TestCase):
    def test_str_representation(self):
        user = User.objects.create_user(username="testuser", password="password")
        seller = Seller.objects.create(seller_name="Mock Seller", user=user)
        self.assertEqual(str(seller), "Mock Seller")


class ProductModelTest(TestCase):
    def test_str_representation(self):
        category = Category.objects.create(name="Electronics")
        user = User.objects.create_user(username="testuser", password="password")
        seller = Seller.objects.create(seller_name="Mock Seller", user=user)
        product = Product.objects.create(
            name="Mock Product",
            price=20.0,
            category=category,
            seller=seller,
        )
        self.assertEqual(str(product), "Mock Product")

    def test_price_is_positive(self):
        category = Category.objects.create(name="Electronics")
        user = User.objects.create_user(username="testuser", password="password")
        seller = Seller.objects.create(seller_name="Mock Seller", user=user)
        product = Product(
            name="Mock Product",
            price=-20.0,  # Negative price is not allowed
            category=category,
            seller=seller,
        )
        with self.assertRaises(ValidationError):
            product.save()

    def test_product_creation(self):
        category = Category.objects.create(name="Electronics")
        user = User.objects.create_user(username="testuser", password="password")
        seller = Seller.objects.create(seller_name="Mock Seller", user=user)
        Product.objects.create(
            name="Mock Product",
            price=20.0,
            category=category,
            seller=seller,
        )
        self.assertEqual(Product.objects.count(), 1)
