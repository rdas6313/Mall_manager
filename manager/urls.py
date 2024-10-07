"""
URL configuration for mall_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:mall_id>/', views.index, name='index'),
    path('<int:mall_id>/create/store',
         views.create_store, name='create_store'),
    path('<int:mall_id>/store/update/<int:store_id>',
         views.update_store, name='update_store'),
    path('<int:mall_id>/store/delete/<int:store_id>',
         views.delete_store, name='delete_store'),

    path('<int:mall_id>/inventory/create',
         views.create_inventory, name='create_inventory'),

    path('<int:mall_id>/inventory/update/<int:inventory_id>',
         views.update_inventory, name='update_inventory'),
    path('<int:mall_id>/inventory/delete/<int:inventory_id>',
         views.delete_inventory, name='delete_inventory'),

    path('<int:mall_id>/employee/create',
         views.create_employee, name='create_employee'),
    path('<int:mall_id>/employee/update/<int:emp_id>',
         views.update_employee, name='update_employee'),
    path('<int:mall_id>/employee/delete/<int:emp_id>',
         views.delete_employee, name='delete_employee'),
    path('<int:mall_id>/customer', views.list_customer, name='customer_list'),
    path('<int:mall_id>/customer/delete/<int:customer_id>',
         views.delete_customer, name='delete_customer')
]
