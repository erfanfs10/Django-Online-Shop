from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from account.models import CustomUser
from product.models import Product


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='basket', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    @classmethod
    def get_basket(cls, request):

        if request.user.is_authenticated:
            try:
                basket = cls.objects.prefetch_related("basket_line").get(user=request.user)
            except cls.DoesNotExist:
                basket = cls.objects.create(user=request.user)
            return basket 

        else:
            try:
                basket_id = request.COOKIES.get("basket_id", None)
                basket = cls.objects.prefetch_related("basket_line").get(pk=basket_id)

            except cls.DoesNotExist :    
               
                response = HttpResponseRedirect(reverse("basket-view"))
                basket = cls.objects.create()
                response.set_cookie("basket_id", basket.id)
                
            return basket
        

class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="basket_line")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket_line")
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.basket}---{self.product}---{str(self.quantity)}"    