from django.urls import path
from django.views.generic import TemplateView
from .views import Categoty, Products, product_detail, search, category_list, rates


urlpatterns = [

    path('', TemplateView.as_view(template_name='product/home.html'), name='home'),
    
    # show's when click on products button on navbar
    path('category_list/', category_list, name='category-list'),

    # show's when click on category, it show's product types of each category
    path('category_list/<str:pk>/', Categoty.as_view(), name='category'),

    # show's all product on specific product type
    path('products/<str:pk>', Products.as_view(), name='products'),

    # show's detail of a product
    path('product/<int:product_id>/', product_detail, name='product-detail'),

    # show's products when you search on navbar
    path('search/', search, name='search'),
    
    # show's user's rates
    path("rates/", rates, name="rates")
]
