from django.contrib import admin
from django.contrib.admin import register
from .models import (Category, Product,
                    ProductAttribute, Brand,
                    ProductAttributeValue,
                    ProductImage, ProductType,
                    Rating, 
                    )


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 3


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 3

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created') 
    inlines = (ProductAttributeInline,)      


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'price', 'status',
                     'brand', 'product_type', 'category')

                     
    search_fields = ('name', 'price', 'brand__name', 'category__name', 'product_type__name')
    list_filter = ('status','category__name')
    list_editable = ('status',)
    inlines = (ProductAttributeValueInline ,ProductImageInline, RatingInline)

@register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("title","body",'product', 'point', 'user', 'created')

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(ProductAttribute)


