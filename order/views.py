from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from basket.models import Basket
from shipping.forms import AddressForm
from shipping.models import Address
from .models import Order, OrderItem



@login_required
def add(request):
    basket = Basket.get_basket(request)
    basket_line = basket.basket_line.select_related("product").all()
    amount = basket.get_total_price(basket_line)

    if Order.objects.filter(user=request.user, status="WP").exists():
        return HttpResponse("You have A Unfinished Order ")
    else:
        order = Order.objects.create(user=request.user, amount=amount)
        for item in basket_line:
            OrderItem.objects.create(order_id=order.id,
                                    product=item.product,
                                    price=item.price,
                                    quantity=item.quantity)
        return redirect('checkout')


class Checkout(LoginRequiredMixin, View):
    template_name = "order/checkout.html"
    form_class = AddressForm

    def get(self, request):
        if Order.objects.filter(user=request.user, status="WP").exists():
            order = Order.objects.filter(user=request.user, status="WP").first()
        else:
            return HttpResponse("You have no order") 
        order_item = order.order_item.select_related("product").all() 
        total_price = 0
        for item in order_item:
            total_price += item.product.price * item.quantity
        total = order_item.count()
        addresses = Address.objects.filter(user=request.user) 
        context = {"order_item": order_item, "addresses": addresses,
                    "form":self.form_class, "total": total, "total_price": total_price}

        return render(request, self.template_name, context)

    def post(self, request):
        pass