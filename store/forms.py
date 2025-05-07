from django import forms

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