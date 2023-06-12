from django.urls import path
from .views import basket_add, basket_delete, basket_view


urlpatterns = [

    path("view/", basket_view, name='basket-view'),
    path("add/", basket_add, name='basket-add'),
    path("delete/<int:product_id>/", basket_delete, name='basket-delete')
]
