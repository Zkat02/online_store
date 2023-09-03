from django.urls import path, include
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
    add_to_cart,
    place_order,
    remove_from_cart,
    create_product,
    manage_orders,
    edit_product,
    ProductsByCategory,
    CustomerList,
    ProductViewSet,
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", product_list, name="home"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("cart/", cart, name="cart"),
    path("order_history/", order_history, name="order_history"),
    path("register/", register_view, name="register"),
    path("register/customer/", register_customer, name="register_customer"),
    path("register/seller/", register_seller, name="register_seller"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path(
        "remove_from_cart/<int:cart_item_id>/",
        remove_from_cart,
        name="remove_from_cart",
    ),
    path("place_order/", place_order, name="place_order"),
    path("create_product/", create_product, name="create_product"),
    path("manage_orders/", manage_orders, name="manage_orders"),
    path("product/<int:product_id>/edit/", edit_product, name="edit_product"),
    path("category/<int:category_id>", ProductsByCategory.as_view(), name="category"),
    path("api/customer_list/", CustomerList.as_view(), name="customer_list"),
]
