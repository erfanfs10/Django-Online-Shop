from django.urls import path
from django.views.generic import TemplateView
from .views import ComponentList, Component, product_detail, products


urlpatterns = [

    path('', TemplateView.as_view(template_name='product/home.html'), name='home'),
    path('products/', products, name='products'),
    path('products/components_list/', ComponentList.as_view(), name='components-list'),
    path('products/components_list/<str:component>', Component.as_view(), name='component'),
    path('product/<int:product_id>/', product_detail, name='product-detail')
    #path('products/gaming/', name='gaming')
    #path('products/networking/', name='networking')
    #path('products/laptop/', name='laptop')
]
