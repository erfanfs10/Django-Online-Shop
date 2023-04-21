from django.urls import path
from .views import AddressView, AddressAdd, AddressDelete, AddressUpdate, AddressCreate


urlpatterns = [
    path("", AddressView.as_view(), name='address-view'),
    path("add/", AddressCreate.as_view(), name="address-add"),
    path("<int:pk>/delete", AddressDelete.as_view(), name="address-delete"),
    path("<int:pk>/update", AddressUpdate.as_view(), name="address-update")
]