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
    def get_basket(cls, request):  # this method allways returns a basket 

        if request.user.is_authenticated:
            try:
                basket = cls.objects.prefetch_related("basket_line").get(user=request.user)
            except cls.DoesNotExist:
                basket = cls.objects.create(user=request.user)
        
        else:
            try:
                basket_id = request.session.get("basket_id", None) # search user session for basket_id cookie
                basket = cls.objects.prefetch_related("basket_line").get(pk=basket_id)
            
            except cls.DoesNotExist : 
                basket = cls.objects.create() 
                request.session["basket_id"] = basket.id  # set basket_id as a cookie for user session

        return basket
    
    @classmethod  
    def get_total_price(cls, basket_line):   # calculate The total Price 
        total = 0
        for line in basket_line:   
            total += line.product.price * line.quantity
        return total    

    def add_to_basket(self, product_id):

        if self.basket_line.filter(product = product_id).exists():
            basket_line = self.basket_line.filter(product = product_id).first()
            basket_line.quantity += 1
            basket_line.save()

        else:
            product = Product.objects.get(pk = product_id)
            basket_line = self.basket_line.create(product = product)    

        return basket_line


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="basket_line")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket_line")
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.basket}---{self.product}---{str(self.quantity)}"    