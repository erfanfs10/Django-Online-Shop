from django.db import models
from account.models import CustomUser
from PIL import Image
import os


class Category(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class ProductType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='product_types', null=True)
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='product_type_images', null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs): # Delete Image From Media File 
        os.remove(self.image.path)
        return super().delete(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Product(models.Model):

    ACTIVE = "AC"
    UNAVAILABLE = "UA"
    COMMING_SOON = "CS"

    STATUS = [
        (ACTIVE, "ACTIVE"),
        (UNAVAILABLE, "UNAVAILABLE"),
        (COMMING_SOON, 'COMMING_SOON')
    ]

    name = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default=ACTIVE)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    view = models.PositiveIntegerField(default=0)
    sell = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-created',)


class ProductAttribute(models.Model):
    name = models.CharField(max_length=30)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='attributes')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.product)} image"
    
    class Meta:
        ordering = ('created',)
    
    def delete(self, *args, **kwargs): # Delete Image From Media File 
        os.remove(self.image.path)
        return super().delete(*args, **kwargs)
       
    def save(self, *args, **kwargs): # reduce product images size using pillow
        super(*args, **kwargs).save()
        with Image.open(self.image.path) as img:
            img.thumbnail((298, 250))
            img.save(str(self.image.path), format="PNG")
       

class ProductAttributeValue(models.Model):
    value = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='values')   
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product}--{self.attribute}--{self.value}"
    

class Rating(models.Model):
    comment = models.TextField(null=True, blank=True)
    point = models.DecimalField(max_digits=10, decimal_places=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='commens')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='comments')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.user.email} {self.point} comment"
    
