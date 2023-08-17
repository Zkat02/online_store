from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Category, Product, Cart, CartItem, Order
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, CustomerRegistrationForm, SellerRegistrationForm
from django.contrib import messages


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(
        request, "product_list.html", {"categories": categories, "products": products}
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "product_detail.html", {"product": product})


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
