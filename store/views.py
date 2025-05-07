from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views import generic
from .forms import *
from .models import *

def index(request):
  template = loader.get_template("index.html")
  return HttpResponse(template.render())

def ProductRegister(request):
  form = ProductForm()
  msg = False
  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name'].lower()
      price = form.cleaned_data['price']
      if Product.objects.filter(name=name).exists():
        msg = {'code': 'danger', 'label': 'Product already exists.'}
      else:
        product = Product(name=name,price=price)
        product.save()
        msg = {'code': 'success', 'label': 'Product has been created.'}
  return render(request, 'product_form.html', {"form": form, "msg": msg})

class ProductListView(generic.ListView):
  model = Product
  queryset = Product.objects.all()
  context_object_name = 'product_list'
  template_name = 'product_list.html'

def ProductUpdate(request, pk):
  try:
    product = Product.objects.get(pk=pk)
  except (Product.DoesNotExist):
    product = None

  if product:
    msg = False
    if request.method == 'POST':
      form = ProductForm(request.POST)
      if form.is_valid():
        product.name = form.cleaned_data['name']
        product.price = form.cleaned_data['price']
        product.save()
        msg = {'code': 'success', 'label': 'Product has been updated.'}
    else:
      form = ProductForm(initial={'name': product.name, 'price': product.price})
  return render(request, "product_update_form.html", {"form": form, "msg": msg})


