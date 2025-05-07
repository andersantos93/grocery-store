from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
  name = models.CharField(max_length=200, unique=True, null=False, help_text="Enter a product")
  price = models.FloatField(null=False, blank=False, default=0.0, validators=[MinValueValidator(0.0)], help_text="Price of the product")
