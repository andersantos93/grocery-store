from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('product/register/', views.ProductRegisterView, name='product-form'),
    path('product/list/', views.ProductListView.as_view(), name='product-list'),
    path('product/update/<int:pk>/', views.ProductUpdateView, name='product-update'),
    path('basket/', views.BasketView, name='customer-basket'),
    path('basket/review', views.BasketReviewListView.as_view(), name='basket-review'),
    path('basket/<int:pk>/approve/', views.BasketApproveView.as_view(), name='basket-approve'),
    path('basket/<int:pk>/deny/', views.BasketDenyView.as_view(), name='basket-deny'),
    path('purchase-history/', views.PurchaseHistoryView.as_view(), name='customer-purchase-history'),
    path('purchase-history/<int:pk>', views.PurchaseHistoryView.as_view(), name='customer-purchase-history'),
    path('customer/list/', views.CustomerListView.as_view(), name='customer-list'),
]
