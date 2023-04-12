from django.contrib import admin
from .models import Basket, BasketLine


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', "user", "created")


@admin.register(BasketLine)
class BasketInlineAdmin(admin.ModelAdmin):
    list_display = ("basket", "product", "quantity")    