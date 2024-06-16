from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender')
        widgets = {
            'gender': forms.Select(choices=User.GENDER_CHOICES),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
