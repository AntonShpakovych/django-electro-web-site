from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from shop.models import Product


class UserLoginForm(forms.Form):
    login = forms.CharField(required=False)
    password = forms.CharField(
        required=False, initial=False, widget=forms.PasswordInput)


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
