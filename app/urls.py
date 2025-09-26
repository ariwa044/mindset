from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('mainnet/', views.mainnet, name='mainnet'),
    path('validate/', views.validate, name='validate'),
    path('payment/', views.payment, name='payment'),
    path('amount/', views.amount, name='amount'),
    path('wallet/', views.wallet, name='wallet'),
]