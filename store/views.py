from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.template import loader
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
import json
import datetime
from .forms import *
from .models import *

def LoginView(request):
  form = LoginForm()
  msg = False
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password']
      )
      if user is not None:
        login(request, user)
        response = redirect("/")
        return response
      else:
        msg = {"code": "danger", "label": "Failed Authentication!"}
  context = {
    'form': form,
    'msg': msg
  }
  return render(request, 'login.html', context)

def LogoutView(request):
  logout(request)
  return redirect("/login")

@login_required
def index(request):
  template = loader.get_template("index.html")
  return HttpResponse(template.render())

@login_required
@permission_required('store.add_product', raise_exception=True)
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

class ProductListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
  model = Product
  queryset = Product.objects.all()
  context_object_name = 'product_list'
  template_name = 'product_list.html'
  permission_required = "store.view_product"

@login_required
@permission_required('store.change_product', raise_exception=True)
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
@permission_required('store.add_basket', raise_exception=True)
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
  return render(request, 'basket.html', {"products": products})

class PurchaseHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
  model = Basket
  context_object_name = 'purchase_history'
  template_name = 'purchase_history.html'
  permission_required = "store.view_basket"

  def get_queryset(self):
    user = self.request.user
    return Basket.objects.filter(customer=user)