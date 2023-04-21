from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.views import View
from .models import Address
from .forms import AddressForm


class AddressView(ListView):
    template_name = "shipping/address_view.html"
    context_object_name = "addresses"

    def get_queryset(self):
        addresses = Address.objects.filter(user=self.request.user)
        return addresses


class AddressAdd(LoginRequiredMixin, View):
    template_name = "shipping/address_add.html"
    form_class = AddressForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('address-view')
        return render(request, self.template_name, {"form": form})


class AddressCreate(LoginRequiredMixin, CreateView):
    model = Address
    fields = ("city", "zipcode", "address")
    template_name_suffix = "_add"
    success_url = reverse_lazy("address-view")

    def form_valid(self, form):
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
