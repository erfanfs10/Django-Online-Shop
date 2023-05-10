from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from .models import Address


class AddressView(ListView):
    template_name = "shipping/address_view.html"
    context_object_name = "addresses"

    def get_queryset(self, *args, **kwargs):
        addresses = Address.objects.filter(user=self.request.user)
        return addresses


class AddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    fields = ("city", "zipcode", "address")
    template_name_suffix = "_add"
    success_url = reverse_lazy("address-view")

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdate(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ("city", "zipcode", "address")
    template_name_suffix = "_update"
    success_url = reverse_lazy("address-view")


class AddressDelete(LoginRequiredMixin, DeleteView):
    model = Address
    template_name_suffix = "_delete"
    success_url = reverse_lazy("address-view")
