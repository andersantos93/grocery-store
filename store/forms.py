from django import forms
from . models import Product

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

# class BasketForm(forms.Form):
  # products = forms.ModelChoiceField(
  #   queryset=Product.objects.all().values(),
  #   required=True,
  #   label="Select a product",
  #   widget=forms.Select(
  #     attrs={"class":"form-control", "name": "price", "placeholder": "Enter product price"}
  #   )
  # )
  # quantity = forms.IntegerField(
  #   required=True, label='Quantity', widget=forms.NumberInput(
  #     attrs={"class":"form-control", "name": "product", "placeholder": "Select the product"}
  #   )
  # )

  # def __init__(self, *args, **kwargs):
  #   super().__init__(*args, **kwargs)
  #   self.fields['products'].label_from_instance = lambda obj: obj.custom_display()