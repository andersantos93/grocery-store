from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Product(models.Model):
  name = models.CharField(max_length=200, unique=True, null=False, help_text="Enter a product")
  price = models.FloatField(null=False, blank=False, default=0.0, validators=[MinValueValidator(0.0)], help_text="Price of the product")
  class Meta:
    ordering = ['name']
  
  def custom_display(self):
    return f"Product: {self.name} | Price: ${self.price}"

class Basket(models.Model):
  customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  products = models.JSONField()
  STATUS = (('a', 'Approved'), ('d', 'Denied'), ('w', 'Waiting for approval'))
  date_created = models.DateField(null=True, blank=True)
  date_modified = models.DateField(null=True, blank=True)