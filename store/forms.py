from django import forms
from . models import Product

class LoginForm(forms.Form):
  username = forms.CharField(
    required=True, label="Enter Username", widget=forms.TextInput(
      attrs={"class":"form-control", "name": "username", "placeholder": "Enter Username"}
    )
  )
  password = forms.CharField(
    required=True, label="Enter Password", widget=forms.PasswordInput(
      attrs={"class":"form-control", "name": "password", "placeholder": "Enter Password"}
    )
  )
class ProductForm(forms.Form):
  name = forms.CharField(
    required=True, label='Name', widget=forms.TextInput(
      attrs={"class":"form-control", "name": "name", "placeholder": "Enter product name"}
    )
  )
  price = forms.FloatField(
    required=True, label='Price', widget=forms.NumberInput(
      attrs={"class":"form-control", "name": "price", "placeholder": "Enter product price"}
    )
  )