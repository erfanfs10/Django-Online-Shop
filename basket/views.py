from django.shortcuts import render, redirect
from django.http import Http404
from .models import Basket


def basket_view(request, *args, **kwargs):
    
    basket = Basket.get_basket(request)     # this method allways returns a basket   
    basket_line = basket.get_basket_line() 
    if basket_line.count() == 0:
        return render(request, "basket/no_item.html")   # returns items in that basket
    total = basket.get_total_price(basket_line)     # calculate The total Price
    context = {"basket_line": basket_line, "total": total}

    return render(request, "basket/basket_view.html", context)


def basket_add(request, *args, **kwargs):

    product_id = request.POST.get("product_id", None)
    quantity = request.POST.get("quantity", None)
    
    if product_id and quantity is None:
        raise Http404

    basket = Basket.get_basket(request)
    basket_line = basket.add_to_basket(product_id, quantity)    # gets a product id and add it to BasketLine Model
    if basket_line == False: 
        raise Http404
    
    http_referer = request.META.get('HTTP_REFERER')
    if http_referer is not None:
        return redirect(request.META.get('HTTP_REFERER'))    #redirect to the same page
    return redirect('basket-view')


def basket_delete(request, product_id, *args, **kwargs):

    basket = Basket.get_basket(request)
    baslet_line = basket.delete_from_basket(product_id)   # gets a product id and delete it from BasketLine Model
    if baslet_line == False:
        raise Http404("SOMETHING WRONG IS HAPPEND")
    
    http_referer = request.META.get('HTTP_REFERER')
    if http_referer is not None:
        return redirect(request.META.get('HTTP_REFERER'))    #redirect to the same page
    return redirect('basket-view')
