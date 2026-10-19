from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class SignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=256, required=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'password1', 'password2')
