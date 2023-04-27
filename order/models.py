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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"order_line {self.order}"
