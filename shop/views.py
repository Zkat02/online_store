from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Category, Product, Cart, CartItem, Order, Seller
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
