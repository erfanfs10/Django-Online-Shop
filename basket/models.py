from django.db import models
from account.models import CustomUser
from product.models import Product


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='basket')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
    


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="basket_line")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket_line")
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.basket}-{self.product}-{str(self.quantity)}"    