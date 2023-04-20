from django.db import models
from account.models import CustomUser


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="addresses")
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=12)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city
