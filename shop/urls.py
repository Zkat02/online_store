from django.urls import path
from .views import *

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('order_history/', order_history, name='order_history'),
]
