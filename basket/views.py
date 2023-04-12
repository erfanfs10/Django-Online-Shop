from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Basket


def basket_view(request):

    if request.user.is_authenticated:
       
        basket = Basket.get_basket(request.user)
        basket_line = basket.basket_line.all()   

    else:
        try:
            basket_id = request.COOKIES.get("basket_id", None)
            basket = Basket.objects.get(pk=basket_id)
            
        except Basket.DoesNotExist :    
            response = HttpResponseRedirect(reverse("basket-view"))
            basket = Basket.objects.create()
            response.set_cookie("basket_id", basket.id)
            return response
        
        basket_line = basket.basket_line.all()
    return render(request, "basket/basket_view.html", {"basket_line": basket_line})


def basket_add(request):
    return HttpResponse(request.user)


def basket_delete(request):
    return HttpResponse(request.user)