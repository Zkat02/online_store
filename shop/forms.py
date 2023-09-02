from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class CustomerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "phone_number", "address"]


class SellerRegistrationForm(UserCreationForm):
    seller_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "seller_name", "address"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image", "quantity"]
