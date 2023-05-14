from django.db import models
from account.models import CustomUser
from product.models import Product


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='basket', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} Basket"
    
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
    

    def get_basket_line(self):
        basket_line = self.basket_line.select_related("product").prefetch_related("product__images").all()
        return basket_line


    @classmethod  
    def get_total_price(cls, basket_line):   # calculate The total Price 
        total = 0
        for line in basket_line:   
            total += line.product.price * line.quantity
        return total    


    def add_to_basket(self, product_id, quantity): #gets a product id and add it to the user BasketLine model

        if self.basket_line.filter(product=product_id).exists():
            basket_line = self.basket_line.filter(product = product_id).first()
            print(quantity)
            if int(quantity) < basket_line.quantity: 
                basket_line.quantity = int(quantity)
            else:
                basket_line.quantity = int(quantity)
            basket_line.save()

        else:
            try:
                product = Product.objects.get(pk = product_id)
                basket_line = self.basket_line.create(product = product, quantity = int(quantity))   
            except Product.DoesNotExist:
                return False
            return basket_line
         

    def delete_from_basket(self, product_id): #gets a product id and delete it to the user BasketLine model

        try:
            product = self.basket_line.get(product=product_id)
        except BasketLine.DoesNotExist:  
            return False
        product.delete()


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="basket_line")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket_line")
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.basket}---{self.product}---{str(self.quantity)}"    