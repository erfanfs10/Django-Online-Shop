from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ProductType, Product
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

class ComponentList(ListView):
    template_name = 'product/components_list.html'
    queryset = ProductType.objects.filter(category__name='component')
    context_object_name = 'components'


class Component(ListView):
    template_name = "product/components.html"
    context_object_name = "products"

    def get_queryset(self):
        context = Product.objects.filter(product_type__name=self.kwargs["component"]).prefetch_related('images') 
        return context      
    

class ProductDetail(DetailView):
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_object(self):
        try:
            obj = Product.objects.filter(pk=self.kwargs["pk"]).prefetch_related("images", "values").first()
        except Product.DoesNotExist:
            return Http404    
        print(obj)
        return obj
