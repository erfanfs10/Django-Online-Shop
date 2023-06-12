from django.urls import path
from .views import Checkout, OrdersView


urlpatterns = [
    path("checkout/", Checkout.as_view(), name="checkout"),
    path("orders/", OrdersView.as_view(), name="orders")
]