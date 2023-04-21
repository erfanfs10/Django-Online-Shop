from django.shortcuts import render
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, ProfileForm


class LoginView(View):
    template_name = "account/login.html"
    form_class = AuthenticationForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        next = request.POST["next"]
        if form.is_valid():
            user = form.get_user()
            login(request, user)
           
            if next:
                return redirect(next)
            return redirect("home")
    
        return render(request, self.template_name, {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return render(request, 'account/logout.html')    


class RegisterView(View):
    template_name = "account/register.html"
    form_class = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {"form": form})


class ProfileView(LoginRequiredMixin, View):
    template_name = "account/profile.html"
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user)
        return render(request, "account/profile.html", {"form": form}) 
    
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        form = ProfileForm(request.POST, instance=request.user)
        return render(request, "account/profile.html", {"form": form}) 
    

class PasswordChangeView(View):
    template_name = "account/changepass.html"
    form_class = PasswordChangeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user)
        return render(request, self.template_name, {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('profile')
        print("dajhfbhajfjrg847857")
        return render(request, self.template_name, {"form": form})



    