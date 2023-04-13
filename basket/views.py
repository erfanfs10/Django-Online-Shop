from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from .models import Basket
from django.shortcuts import redirect
from product.models import Product
from django.db.models import Sum


def basket_view(request):
   
    basket = Basket.get_basket(request)  # this method returns allways a basket   
    basket_line = basket.basket_line.all()
    total = basket_line.aggregate(total=Sum("product__price"))
    print(total["total"])
    return render(request, "basket/basket_view.html", {"basket_line": basket_line, "total": total})


def basket_add(request, product_id):

    basket = Basket.get_basket(request)
    if basket.basket_line.filter(product = product_id).exists():
        basket_line = basket.basket_line.filter(product = product_id).first()
        basket_line.quantity += 1
        basket_line.save()

    else:
        product = Product.objects.get(pk = product_id)
        basket_line = basket.basket_line.create(product = product)    
    return redirect('basket-view')


def basket_delete(request, product_id):
    return HttpResponse(product_id)