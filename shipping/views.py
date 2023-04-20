from django.shortcuts import render, redirect, get_object_or_404
from .models import Address
from .forms import AddressForm
from django.contrib.auth.decorators import login_required


def address_view(request):

    addresses = Address.objects.filter(user=request.user)

    return render(request, "shipping/address_view.html", {"addresses": addresses})


@login_required()
def address_add(request):

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('address-view')

    form = AddressForm()

    return render(request, "shipping/address_add.html", {"form": form})        


@login_required
def address_delete(request, pk):

    address = get_object_or_404(Address, pk=pk)
    address.delete()

    return redirect("address-view")
