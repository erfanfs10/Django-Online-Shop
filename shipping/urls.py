from django.urls import path
from .views import AddressView, AddressAdd, AddressDelete, AddressUpdate


urlpatterns = [

    path("view/", AddressView.as_view(), name='address-view'),
    path("add/", AddressAdd.as_view(), name="address-add"),
    path("delete/<int:pk>", AddressDelete.as_view(), name="address-delete"),
    path("update/<int:pk>", AddressUpdate.as_view(), name="address-update")



]