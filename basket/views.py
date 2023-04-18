from django.shortcuts import render, redirect
from .models import Basket


def basket_view(request):
   
    basket = Basket.get_basket(request)  # this method allways returns a basket   
    basket_line = basket.basket_line.select_related("product").prefetch_related("product__images").all()
    total = Basket.get_total_price(basket_line)  # calculate The total Price
    context = {"basket_line": basket_line, "total": total}

    return render(request, "basket/basket_view.html", context)


def basket_add(request, product_id):

    basket = Basket.get_basket(request)
    basket.add_to_basket(product_id) # gets a product id and add it to BasketLine Model
      
    return redirect(request.META.get('HTTP_REFERER'))


def basket_delete(request, product_id):

    basket = Basket.get_basket(request)
    basket.delete_from_basket(product_id) # gets a product id and delete it from BasketLine Model
    
    return redirect(request.META.get('HTTP_REFERER'))
