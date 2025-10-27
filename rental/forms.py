from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Car

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        validators=[UnicodeUsernameValidator()],
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        widget=forms.TextInput(
            attrs={
                'pattern': r'^[\w.@+-]+$',
                'title': 'Use letters, numbers, and @/./+/-/_ only.'
            }
        ),
    )
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('NormalUser', 'Normal User'), ('Manager', 'Manager')])

    class Meta:
        model=User
        fields=('username','email','password1','password2','role')

class CarForm(forms.ModelForm):
    class Meta:
        model= Car
        fields=('name','description','price_per_day','is_available','image')
