from django.urls import path
from .views import address_view, address_add, address_delete


urlpatterns = [

    path("view/", address_view, name='address-view'),
    path("add/", address_add, name="address-add"),
    path("delete/<int:pk>", address_delete, name="address-delete")


]