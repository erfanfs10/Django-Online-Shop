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
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='orders', null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    shipping_price = models.SmallIntegerField(default=0)
    status = models.CharField(max_length=2, default=WAITING_FOR_PAY, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} order with {self.amount} $"

    @classmethod
    def get_total_price(self, order_item):
        total_price = 0
        for item in order_item:
            total_price += item.product.price * item.quantity
        return total_price
    
    @classmethod
    def get_order(cls, request, amount):
        if cls.objects.filter(user=request.user, status="WP").exists():
            order = cls.objects.filter(user=request.user, status="WP").first()
            order.delete()
        order = cls.objects.create(user=request.user, amount=amount)
        return order

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
