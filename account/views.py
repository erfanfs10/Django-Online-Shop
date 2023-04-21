from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.forms import AuthenticationForm


class LoginView(View):
    template_name = "account/login.html"
    form_class = AuthenticationForm
    
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
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



def register_view(request):
    context = {}
    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            login(request, user)
            return redirect("home")
        else:
            context["form"] = form
    
    else:
        form = CustomUserCreationForm
        return render(request, "account/register.html", {"form": form})
    
    return render(request, "account/register.html", context)


@login_required
def profile(request):

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        form = ProfileForm(request.POST, instance=request.user)

    else:
        form = ProfileForm(instance=request.user)
        return render(request, "account/profile.html", {"form": form}) 

    return render(request, "account/profile.html", {"form": form}) 
       