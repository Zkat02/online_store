from django.test import TestCase, Client
from django.urls import reverse


class TestView(TestCase):
    def test_product_list_GET(self):
        cl = Client()
        response = cl.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_list.html")
