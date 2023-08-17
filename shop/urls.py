from django.urls import path
from .views import (
    product_list,
    product_detail,
    cart,
    order_history,
    register_view,
    register_customer,
    register_seller,
    login_view,
    logout_view,
)

urlpatterns = [
    path("", product_list, name="home"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("cart/", cart, name="cart"),
    path("order_history/", order_history, name="order_history"),
    path("register/", register_view, name="register"),
    path("register/customer/", register_customer, name="register_customer"),
    path("register/seller/", register_seller, name="register_seller"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
