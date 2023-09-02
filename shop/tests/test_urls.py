from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop.views import (
    product_list,
    # product_detail,
    # cart,
    # order_history,
    # register_view,
    # register_customer,
    # register_seller,
    # login_view,
    # logout_view,
)


class TestUrls(SimpleTestCase):
    def test_list_url_is_resolve(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, product_list)
