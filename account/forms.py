from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("name", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("name", "email", "phone_number")   

    #validate phone number
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]  
        try:
            int(phone_number)
        except ValueError:
            self.errors['phone_number'] = ['The Phone Number Is Not Valid! ']
            return phone_number
        if phone_number[0:2] != "09" or len(phone_number) < 11:
            self.errors['phone_number'] = ['The Phone Number Is Not Valid! ']
        return phone_number   
     