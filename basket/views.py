from django.shortcuts import render
from django.http import HttpResponse
from .models import Basket
from django.shortcuts import redirect
from product.models import Product


def basket_view(request):
   
    basket = Basket.get_basket(request)  # this method allways returns a basket   
    basket_line = basket.basket_line.select_related("product").all()
    total = Basket.get_total_price(basket_line)  # calculate The total Price
    context = {"basket_line": basket_line, "total": total}

    return render(request, "basket/basket_view.html", context)


def basket_add(request, product_id):

    basket = Basket.get_basket(request)
    basket_line = basket.add_to_basket(product_id) # gets a product id and add it to basket_line model
      
    return redirect(request.META.get('HTTP_REFERER'))


def basket_delete(request, product_id):

    return HttpResponse(product_id)