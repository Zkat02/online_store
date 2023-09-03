from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Customer,
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Seller,
)
from django.views.generic import ListView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    UserLoginForm,
    CustomerRegistrationForm,
    SellerRegistrationForm,
    ProductForm,
)
from django.contrib import messages
from decimal import Decimal
from django.db import transaction
from .serializers import CustomerSerializer, ProductSerializer
from rest_framework import generics, mixins
from rest_framework.viewsets import GenericViewSet

# from rest_framework.permissions import IsAdminUser


class CustomerList(generics.ListCreateAPIView):
    # ListCreateAPIView: provides get and post method handlers.

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAdminUser]


class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsByCategory(ListView):
    model = Product
    template_name = "products_list_by_category.html"
    context_object_name = "products"
    allow_empty = False
    # paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_name"] = Category.objects.get(
            pk=self.kwargs["category_id"]
        ).name
        return context

    def get_queryset(self):
        return Product.objects.filter(
            category_id=self.kwargs["category_id"]
        ).select_related("category")


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(
        request, "product_list.html", {"categories": categories, "products": products}
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "product_detail.html", {"product": product})


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        customer = request.user.customer

        cart, created = Cart.objects.get_or_create(customer=customer)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, quantity=1
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("cart")

    else:
        return redirect("login")


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.cart.customer.user != request.user:
        messages.error(
            request, "You don't have permission to remove this item from the cart."
        )

    cart_item.delete()
    messages.success(request, "Product has been removed from your cart.")
    return redirect("cart")


def place_order(request):
    if request.method == "POST":
        selected_items = request.POST.getlist("selected_items")

        if not selected_items:
            messages.error(request, "Choose at least one product")
            return redirect("cart")

        with transaction.atomic():
            order = Order(customer=request.user.customer, total_price=Decimal("0.00"))
            order.save()
            for item_id in selected_items:
                cart_item = CartItem.objects.get(id=item_id)
                quantity = int(
                    request.POST.get(f"quantity_{item_id}", cart_item.quantity)
                )
                if quantity > 0:
                    product = cart_item.product
                    if quantity <= product.quantity:
                        order_item = OrderItem(
                            order=order, product=product, quantity=quantity
                        )
                        order_item.save()
                        order.total_price += product.price * quantity
                        cart_item.delete()
                        product.quantity -= quantity
                        product.save()
                    else:
                        messages.error(request, "Sorry... :( \n Product out of stock")
                        return redirect("cart")
            order.save()
        messages.success(request, "Your order is processed")
        return redirect("order_history")
    else:
        return redirect("cart")


@login_required
def cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, "cart.html", {"cart": cart, "cart_items": cart_items})


@login_required
def order_history(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer)
    return render(request, "order_history.html", {"orders": orders})


def register_view(request):
    return render(request, "auth/register_choise.html")


def register_customer(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = Customer(
                user=user,
                phone_number=form.cleaned_data["phone_number"],
                address=form.cleaned_data["address"],
            )
            customer.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomerRegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def register_seller(request):
    if request.method == "POST":
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            seller = Seller(
                user=user,
                seller_name=form.cleaned_data["seller_name"],
                address=form.cleaned_data["address"],
            )
            seller.save()
            login(request, user)
            return redirect("home")
    else:
        form = SellerRegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are in system!")
            return redirect("home")
        else:
            messages.error(request, "Error due to login!")
    else:
        form = UserLoginForm()
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            return redirect("home")
    else:
        form = ProductForm()

    return render(request, "create_product.html", {"form": form})


@login_required
def manage_orders(request):
    seller = request.user.seller
    orders = Order.objects.filter(orderitem__product__seller=seller).distinct()
    return render(request, "manage_orders.html", {"orders": orders})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user != product.seller.user:
        messages.error(request, "You don't have permission to edit this product.")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_detail", product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {"form": form, "product": product})
