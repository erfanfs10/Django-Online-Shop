from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.http import require_GET
from django.db.models import Q
from .models import ProductType, Product


@require_GET
def search(request, *args, **kwargs):
    q = request.GET.get('q', None)
    products = Product.objects.filter(Q(name__icontains=q) |
                                       Q(brand__name__icontains=q) |
                                         Q(product_type__name__icontains=q))
    return render(request, "product/product_search.html", {"products": products})


@require_GET
def category_list(request, *args, **kwargs):
     return render(request, "product/category_list.html")


class Categoty(ListView):
    template_name = 'product/product_types.html'
    context_object_name = 'product_types'

    def get_queryset(self, *args, **kwargs):
        context = ProductType.objects.filter(category__name=self.kwargs["pk"])
        return context      


class Products(ListView):
    template_name = "product/products.html"
    context_object_name = "products"

    def get_queryset(self, *args, **kwargs):
        order_by = self.request.GET.get("q", "created")
        context = Product.objects.filter(product_type__name=self.kwargs["pk"]).prefetch_related('images').order_by("-"+order_by)
        return context   

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)  
        context["type"] = self.kwargs["pk"] 
        return context

    

@require_GET
def product_detail(request, product_id, *args, **kwargs):
   
    product = Product.objects.filter(pk=product_id).prefetch_related("images", "values", "values__attribute").first()
    product.view += 1
    product.save()
    return render(request, "product/product_detail.html", {"product": product})
    