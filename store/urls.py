from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/register/', views.ProductRegisterView, name='product-form'),
    path('product/list/', views.ProductListView.as_view(), name='product-list'),
    path('product/update/<int:pk>/', views.ProductUpdateView, name='product-update'),
    path('customer/basket/', views.BasketView, name='customer-basket'),
    path('customer/purchase-history/', views.CustomerPurchaseHistoryView.as_view(), name='customer-purchase-history'),
]
