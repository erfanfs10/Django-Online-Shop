from django.urls import path
from .views import Checkout, add


urlpatterns = [
    #path("view/", order_view, name="order-view"),
    path("add/", add, name="order-add"),
    path("checkout/", Checkout.as_view(), name="checkout"),
]