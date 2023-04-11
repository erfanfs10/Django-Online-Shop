from django.contrib import admin
from django.contrib.admin import register
from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "phone_number", "date_joined", "is_active")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    
    

