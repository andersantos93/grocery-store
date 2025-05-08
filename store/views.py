from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.template import loader
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
import json
import datetime
from .forms import *
from .models import *

def index(request):
  template = loader.get_template("index.html")
  return HttpResponse(template.render())

def ProductRegisterView(request):
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

def ProductUpdateView(request, pk):
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

@csrf_protect
@login_required
def BasketView(request):
  products = Product.objects.all().values()
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      if not isinstance(data, list):
          return JsonResponse({'error': 'Expected a list of items'}, status=400)
      
      for item in data:
        if not all(k in item for k in ('id', 'name', 'quantity')):
          return JsonResponse({'error': f'Missing fields in item: {item}'}, status=400)
        
        try:
          current_date = datetime.date.today()
          basket = Basket(
            products=data,
            date_created=current_date,
            customer=request.user,
          )
          basket.save()
          return JsonResponse({'message': 'success'}, status=200)
        except json.JSONDecodeError:
          return JsonResponse({'error': 'Error requesting service, please try again.'}, status=500)
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON'}, status=400)
  return render(request, 'customer/basket.html', {"products": products})

class CustomerPurchaseHistoryView(generic.ListView):
  model = Basket
  context_object_name = 'purchase_history'
  template_name = 'customer/purchase_history.html'

  def get_queryset(self):
    user = self.request.user
    return Basket.objects.filter(customer=user)