from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Car

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('NormalUser', 'Normal User'), ('Manager', 'Manager')])

    class Meta:
        model=User
        fields=('username','email','password1','password2','role')

class CarForm(forms.ModelForm):
    class Meta:
        model= Car
        fields=('name','description','price_per_day','is_available','image')
