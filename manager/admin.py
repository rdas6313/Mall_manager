from django.contrib import admin
from . import models
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

# Register your models here.


@admin.register(models.Mall)
class MallAdmin(admin.ModelAdmin):
    list_display = ['name',  'customer_count', 'inventory_count']
    list_per_page = 10
    ordering = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('inventories', 'customers')

    @admin.display(ordering='customers')
    def customer_count(self, mall):
        url = (reverse('admin:manager_customer_changelist')
               + '?'
               + urlencode({'mall': mall.id}))
        html = format_html(
            '<a href="{}">{}</a>', url, mall.customers.count())
        return html

    @admin.display(ordering='inventories', description='Inventory count')
    def inventory_count(self, mall):
        return mall.inventories.count()


@admin.register(models.Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']
    list_per_page = 10
    ordering = ['name', 'quantity']


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'lease_start', 'lease_end', 'mall_name']
    list_per_page = 10
    ordering = ['lease_start', 'lease_end']
    list_select_related = ['mall']

    def mall_name(self, store):
        return store.mall.name


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'store_name', 'mall_name']
    list_per_page = 10
    ordering = ['name']
    list_select_related = ['mall', 'store']

    @admin.display(ordering='store')
    def store_name(self, emp):
        return emp.store.name

    @admin.display(ordering='mall')
    def mall_name(self, emp):
        return emp.mall.name


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'last_visit']
    list_per_page = 10
