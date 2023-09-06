from django.test import TestCase
from shop.serializers import ProductSerializer
from django.contrib.auth.models import User
from shop.models import Seller  # , Category
from decimal import Decimal


class TestProductSerializer(TestCase):
    def setUp(self):
        # self.category = Category.objects.create(name="test")
        self.user = User.objects.create_user(username="testuser", password="test")
        self.seller = Seller.objects.create(seller_name="test seller", user=self.user)

    def test_product_validate_price_negative(self):
        product_data = {
            "name": "test product",
            "description": "Test description",
            "price": Decimal(-10.00),
            "category": {"name": "test category", "id": 1},
            # "category": {"name": self.category.name, "id": self.category.id},
            "seller": self.seller.id,
            "quantity": 5,
        }
        serializer = ProductSerializer(data=product_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue("price" in serializer.errors)

    def test_product_validate_price_valid(self):
        product_data = {
            "name": "test product",
            "description": "Test description",
            "price": Decimal(10.00),
            "category": {"name": "test category", "id": 1},
            # "category": {"name": self.category.name, "id": self.category.id},
            "seller": self.seller.id,
            "quantity": 5,
        }
        serializer = ProductSerializer(data=product_data)
        self.assertTrue(serializer.is_valid())
