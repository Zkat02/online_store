from django.shortcuts import render, get_object_or_404
from .models import Customer, Seller, Category, Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product_list.html', {'categories': categories, 'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items})


@login_required
def order_history(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'order_history.html', {'orders': orders})
