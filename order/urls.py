from django.urls import path
from .views import Checkout, order_add, order_delete


urlpatterns = [
    #path("view/", order_view, name="order-view"),
    path("add/", order_add, name="order-add"),
    path("delete/", order_delete, name="order-delete"),
    path("checkout/", Checkout.as_view(), name="checkout"),
]