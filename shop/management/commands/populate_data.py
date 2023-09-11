import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import (
    Customer,
    Seller,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


class Command(BaseCommand):
    help = "Populates sample data into the database"

    DATA_PATH = "shop/management/commands/data/"

    def load_json_data(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
        return data

    def create_users(self):
        user_data = self.load_json_data(f"{self.DATA_PATH}users.json")
        for data in user_data:
            username = data["username"]
            if not User.objects.filter(username=username).exists():
                User.objects.create(username=username)
                self.stdout.write(self.style.SUCCESS(f"User {username} created"))

    def create_categories(self):
        category_data = self.load_json_data(f"{self.DATA_PATH}categories.json")
        for data in category_data:
            name = data["name"]
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(name=name)
                self.stdout.write(self.style.SUCCESS(f"Category {name} created"))

    def create_sellers(self):
        seller_data = self.load_json_data(f"{self.DATA_PATH}sellers.json")
        for data in seller_data:
            username = data["username"]
            if not Seller.objects.filter(user__username=username).exists():
                user = User.objects.get(username=username)
                Seller.objects.create(
                    user=user, seller_name=data["seller_name"], address=data["address"]
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Seller {data["seller_name"]} created')
                )

    def create_customers(self):
        customer_data = self.load_json_data(f"{self.DATA_PATH}customers.json")
        for data in customer_data:
            username = data["username"]
            if not Customer.objects.filter(user__username=username).exists():
                user = User.objects.get(username=username)
                Customer.objects.create(
                    user=user,
                    phone_number=data["phone_number"],
                    address=data["address"],
                )
                self.stdout.write(self.style.SUCCESS(f"Customer {username} created"))

    def create_products(self):
        product_data = self.load_json_data(f"{self.DATA_PATH}products.json")
        for data in product_data:
            category = Category.objects.get(name=data["category_name"])
            seller = Seller.objects.get(user__username=data["seller_username"])
            if not Product.objects.filter(name=data["name"]).exists():
                Product.objects.create(
                    name=data["name"],
                    description=data["description"],
                    price=data["price"],
                    category=category,
                    seller=seller,
                    quantity=data["quantity"],
                )
                self.stdout.write(self.style.SUCCESS(f'Product {data["name"]} created'))

    def create_carts(self):
        cart_data = self.load_json_data(f"{self.DATA_PATH}carts.json")
        for data in cart_data:
            customer = Customer.objects.get(user__username=data["customer_username"])
            if not Cart.objects.filter(customer=customer).exists():
                Cart.objects.create(customer=customer)
                self.stdout.write(
                    self.style.SUCCESS(f'Cart created for {data["customer_username"]}')
                )

    def create_cart_items(self):
        cart_item_data = self.load_json_data(f"{self.DATA_PATH}cart_items.json")
        for data in cart_item_data:
            cart = Cart.objects.get(
                customer__user__username=data["cart_customer_username"]
            )
            product = Product.objects.get(name=data["product_name"])
            if not CartItem.objects.filter(cart=cart, product=product).exists():
                CartItem.objects.create(
                    cart=cart, product=product, quantity=data["quantity"]
                )
                self.stdout.write(
                    self.style.SUCCESS(f'CartItem created for {data["product_name"]}')
                )

    def create_orders(self):
        order_data = self.load_json_data(f"{self.DATA_PATH}orders.json")
        for data in order_data:
            customer = Customer.objects.get(user__username=data["customer_username"])
            if not Order.objects.filter(customer=customer).exists():
                Order.objects.create(customer=customer, total_price=data["total_price"])
                self.stdout.write(
                    self.style.SUCCESS(f'Order created for {data["customer_username"]}')
                )

    def create_order_items(self):
        order_item_data = self.load_json_data(f"{self.DATA_PATH}order_items.json")
        for data in order_item_data:
            order = Order.objects.get(
                customer__user__username=data["order_customer_username"]
            )
            product = Product.objects.get(name=data["product_name"])
            if not OrderItem.objects.filter(order=order, product=product).exists():
                OrderItem.objects.create(
                    order=order, product=product, quantity=data["quantity"]
                )
                self.stdout.write(
                    self.style.SUCCESS(f'OrderItem created for {data["product_name"]}')
                )

    def handle(self, *args, **options):
        self.create_users()
        self.create_categories()
        self.create_sellers()
        self.create_customers()
        self.create_products()
        self.create_carts()
        self.create_cart_items()
        self.create_orders()
        self.create_order_items()

        self.stdout.write(self.style.SUCCESS("Sample data populated successfully"))
