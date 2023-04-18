from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomUserCreationForm


def login_view(request):

    if request.method == 'POST':

        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        msg = 'Please enter a correct email and password. Note that both fields may be case-sensitive.' 
        messages.warning(request, msg)
        return redirect('login')  
    
    else:     
       return render(request, 'account/login.html')


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
