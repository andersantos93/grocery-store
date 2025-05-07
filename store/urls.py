from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/register/', views.ProductRegister, name='product-form'),
    path('product/list/', views.ProductListView.as_view(), name='product-list'),
    path('product/update/<int:pk>/', views.ProductUpdate, name='product-update')
]
