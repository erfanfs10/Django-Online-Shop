from django.db import models
from account.models import CustomUser
from shipping.models import Address
from product.models import Product

class Order(models.Model):

    WAITING_FOR_PAY = "WP"
    PAYED = "PD"
    SENDING = "SE"
    DELIVERED = "DE"

    STATUS = (
        (WAITING_FOR_PAY, "WAITING_FOR_PAY"),
        (PAYED, "PAYED"),
        (SENDING, "SENDING"),
        (DELIVERED, "DELIVERED")
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='orders', null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    shipping_price = models.SmallIntegerField(default=0)
    status = models.CharField(max_length=2, default=WAITING_FOR_PAY, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} order with {self.amount} $"


    @classmethod
    def get_order(cls, request):
        orders = cls.objects.prefetch_related("order_item__product").filter(user=request.user).all()
        return orders


    @classmethod
    def add_order(cls, request, basket, basket_line, amount, address):
        order = cls.objects.create(user=request.user, amount=amount, address=address)
        order.add_order_item(basket_line)
        basket.delete()
        

    def get_order_item(self):
        order_item = self.order_item.select_related("product").all() 
        return order_item
    

    def add_order_item(self, basket_line):
        for item in basket_line:
            self.order_item.create(order_id=self.id,
                                    product=item.product,
                                    price=item.product.price,
                                    quantity=item.quantity)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"order_line {self.order}"
