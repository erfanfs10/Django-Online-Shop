from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from basket.models import Basket
from shipping.models import Address
from .models import Order


class Checkout(LoginRequiredMixin, View):
    template_name = "order/checkout.html"

    def get(self, request, *args, **kwargs):

        basket = Basket.get_basket(request)
        basket_line = basket.basket_line.select_related("product").all()
        if basket_line.count() == 0:
            return render(request, "order/no_order.html")
        
        amount = basket.get_total_price(basket_line)    
        total_item = basket.get_total_item(basket_line) #basket_line.count()
        addresses = Address.objects.filter(user=request.user)

        context = {"basket_line": basket_line, "addresses": addresses,
                   "total_item": total_item, "total_price": amount}
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        
        address = get_object_or_404(Address, pk=request.POST["address"])
        basket = Basket.get_basket(request)
        basket_line = basket.basket_line.select_related("product").all()
        amount = basket.get_total_price(basket_line)    

        Order.add_order(request, basket, basket_line, amount, address)

        '''
        in this stage we must redirect user to the payment page,
        i don't have any payment page and gateway so i redirect user
        to the order history again!  
        '''

        return redirect("orders")
    

class OrdersView(LoginRequiredMixin, ListView):
    template_name = "order/order_view.html"   
    context_object_name = "orders"

    def get_queryset(self):
        orders = Order.get_order(self.request)
        return orders