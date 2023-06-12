from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from .models import ProductType, Product, Rating
from .forms import RatingForm


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
        context = Product.objects.filter(product_type__name=self.kwargs["pk"]).prefetch_related('images').annotate(point=Avg("comments__point")).order_by("-"+order_by)
        return context   

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)  
        context["type"] = self.kwargs["pk"] 
        return context

    

def product_detail(request, product_id, *args, **kwargs):
    product = Product.objects.filter(pk=product_id).prefetch_related("images", "values", "values__attribute", "comments").first()
    rates = product.comments.all()
    product.view += 1
    product.save()
    context = {"product": product, "rates": rates, "form": RatingForm(initial={"point": 1})}

    if request.method == "POST":
        if not request.user.is_authenticated: # the user must login to rate
            return redirect("login")
        form = RatingForm(request.POST)

        can_rate = form.check_buy(request.user, product, form)

        """
            the check_buy method checks if user bought that product or not
            because only users that bought that product can rate .
            it returns True or False and store it in can_rate variable.
        """

        if can_rate:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.product = product
                instance.save()
                return redirect(request.META.get('HTTP_REFERER'))  
        context["form"] = form  
       
    return render(request, "product/product_detail.html", context)


@login_required
def rates(request):
    rates = Rating.objects.filter(user=request.user).select_related("product")
    return render(request, "product/rates.html", {"rates": rates})