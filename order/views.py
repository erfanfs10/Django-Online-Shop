from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from basket.models import Basket
from shipping.forms import AddressForm
from shipping.models import Address
from .models import Order, OrderItem


@login_required
def order_add(request):
    basket = Basket.get_basket(request)
    basket_line = basket.basket_line.select_related("product").all()
    amount = basket.get_total_price(basket_line)

    if Order.objects.filter(user=request.user, status="WP").exists():
        return redirect('checkout')
    else:
        if basket_line:
            order = Order.objects.create(user=request.user, amount=amount)
            for item in basket_line:
                OrderItem.objects.create(order_id=order.id,
                                        product=item.product,
                                        price=item.product.price,
                                        quantity=item.quantity)
            return redirect('checkout')
        return render(request, "order/nothing_in_basket.html")


@login_required
def order_delete(request):
    order = get_object_or_404(Order, user=request.user)
    order.delete()
    return redirect("basket-view")


class Checkout(LoginRequiredMixin, View):
    template_name = "order/checkout.html"

    def get(self, request, *args, **kwargs):

        if Order.objects.filter(user=request.user, status="WP").exists():
            order = Order.objects.filter(user=request.user, status="WP").first()
        else:
            return render(request, "order/no_order.html")
        
        order_item = order.order_item.select_related("product").all() 
        total_price = Order.get_total_price(order_item)
        total_item = order_item.count()
        addresses = Address.objects.filter(user=request.user)
        context = {"order_item": order_item, "addresses": addresses,
                   "total_item": total_item, "total_price": total_price}
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        address = get_object_or_404(Address, pk=request.POST["address"])
        order = Order.objects.filter(user=request.user, status="WP").update(address=address)

        '''
        in this stage we must redirect user to the payment page,
        i don't have any payment page and gateway so i redirect user
        to the checkout url again!  
        '''

        return redirect("checkout")