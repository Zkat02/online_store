from django.test import TestCase
from shop.models import Category


class FixtureTestCase(TestCase):
    fixtures = ["categories"]  # Specify the fixture file

    def test_category_count(self):
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 2)
