from django.contrib import admin
from .models import Product, Basket

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'price')

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
  list_display = ('customer', 'products', 'status', 'date_created', 'date_modified')

