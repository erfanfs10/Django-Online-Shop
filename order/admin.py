from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "amount", "shipping_price", "status")
    list_filter = ("status",)
    list_editable = ("status",)
    inlines = (OrderItemInline,)