from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from shop.models import Product, Category, Seller
from django.urls import reverse


class ViewTestCase(TestCase):
    @patch("shop.views.get_object_or_404")
    def test_product_detail_view(self, mock_get_object_or_404):
        # create mock objects for create mock Product
        mock_category = Category.objects.create(name="Electronics")
        mock_user = User.objects.create_user(username="mockuser", password="password")
        mock_seller = Seller.objects.create(seller_name="Mock Seller", user=mock_user)
        mock_product = Product(
            name="Mock Product",
            price=20.0,
            category=mock_category,
            seller=mock_seller,
        )
        mock_product.save()  # save mock object to assign an id

        mock_get_object_or_404.return_value = mock_product

        response = self.client.get(reverse("product_detail", args=[mock_product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, mock_product.name)
