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
    SellerReport,
    User,
)
from django.views.generic import ListView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    UserLoginForm,
    CustomerRegistrationForm,
    SellerRegistrationForm,
    ProductForm,
    ReportForm,
)
from django.contrib import messages
from decimal import Decimal
from django.db import transaction
from .serializers import ProductSerializer, CategorySerializer, UserCustomerSerializer, UserSellerSerializer, CustomerSerializer
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import JsonResponse
from .tasks import generate_seller_report
from celery.result import AsyncResult
from djoser.views import TokenCreateView
from rest_framework_simplejwt.tokens import RefreshToken

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class CustomerRegistrationView(APIView):
    # {
    #     "email": "example@example.com",
    #     "username": "example_user",
    #     "password": "your_password",
    #     "customer": {
    #         "phone_number": "1234567890",
    #         "address": "123 Main Street"
    #     }
    # }
    def post(self, request):
        serializer = UserCustomerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.id,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellerRegistrationView(APIView):
    # {
    #     "seller": {
    #           "seller_name": "Example Seller",
    #           "address": "123 Seller Street"
    #     },
    #     "email": "seller@example.com",
    #     "username": "seller_username",
    #     "password": "seller_password"
    # }
    def post(self, request):
        serializer = UserSellerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.id,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCustomerViewSet(viewsets.ModelViewSet):
    # represent user linked with customer
    queryset = User.objects.all()
    serializer_class = UserCustomerSerializer

class UserSellerViewSet(viewsets.ModelViewSet):
    # represent user linked with customer
    queryset = User.objects.all()
    serializer_class = UserSellerSerializer


def seller_report(request, seller_id):
    # start Celery task
    task_result = generate_seller_report.delay(seller_id, request.user.id)

    # Save task_id in session or in BD
    request.session["task_id"] = task_result.id

    return JsonResponse(
        {
            "task_id": task_result.id,
            "get_task_result": f"http://localhost:8000/get_task_result/{task_result.id}",
        }
    )


def get_task_result(request, task_id):
    task = AsyncResult(task_id)
    # checking of task status (PENDING', 'SUCCESS', 'FAILURE' and ...)
    if task.state == "SUCCESS":
        return JsonResponse({"status": "SUCCESS", "result": task.result})
    elif task.state == "FAILURE":
        return JsonResponse({"status": "FAILURE", "error_message": task.result})
    else:
        # the task is still running or in the queue, return the status
        return JsonResponse({"status": task.state})


def create_and_list_reports(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            seller = form.cleaned_data["seller"]

            # start Celery task
            task_result = generate_seller_report.delay(
                seller.id, request.user.id, title
            )
            # save task_id in session (may in BD)
            request.session["task_id"] = task_result.id

            messages.success(
                request,
                "Your report is being created. It will be available in your reports.",
            )
            return redirect("create_and_list_reports")
    else:
        form = ReportForm()

    # Получение списка отчетов пользователя
    reports = SellerReport.objects.filter(user=request.user)

    return render(
        request, "create_and_list_reports.html", {"form": form, "reports": reports}
    )


def report_detail(request, report_id):
    report = SellerReport.objects.get(id=report_id)
    task = AsyncResult(report.task_id)

    if task.state == "SUCCESS":
        context = {
            "report": report,
            "task_status": task.state,
            "task_result": task.result,
        }
        return render(request, "report_detail.html", context)
    elif task.state == "FAILURE":
        return JsonResponse({"status": "FAILURE", "error_message": task.result})
    else:
        return JsonResponse({"status": task.state})


def delete_report(request, report_id):
    report = SellerReport.objects.get(id=report_id)
    report.delete()
    return redirect("create_and_list_reports")


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


# @cache_page(CACHE_TTL)
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
