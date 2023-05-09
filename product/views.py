from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from .models import ProductType, Product


def products(request):
    q = request.GET.get('q', None)
    products = Product.objects.filter(name__icontains=q)
    return render(request, "product/product_search.html", {"products": products})


@cache_page(300)
def products_list(request):
     return render(request, "product/products_list.html")


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
    

def product_detail(request, product_id):
   
    product = Product.objects.filter(pk=product_id).prefetch_related("images", "values", "values__attribute").first()
    product.view += 1
    product.save()
    return render(request, "product/product_detail.html", {"product": product})
    