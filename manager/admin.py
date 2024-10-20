from django.contrib import admin
from . import models
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from .Filters import QuantityFilter

# Register your models here.


class StoreInline(admin.StackedInline):
    model = models.Store
    min_num = 1
    extra = 0


@admin.register(models.Mall)
class MallAdmin(admin.ModelAdmin):
    list_display = ['name',  'customer_count', 'inventory_count']
    list_per_page = 10
    ordering = ['name']
    search_fields = ['name__istartswith']
    autocomplete_fields = ['customers', 'inventories']
    inlines = [StoreInline]

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
        url = (reverse('admin:manager_inventory_changelist')
               + '?'
               + urlencode({'mall': mall.id}))
        html = format_html(
            '<a href="{}">{}</a>', url, mall.inventories.count())
        return html


@admin.register(models.Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']
    list_per_page = 10
    ordering = ['name', 'quantity']
    search_fields = ['name__istartswith']
    list_filter = [QuantityFilter]


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'lease_start', 'lease_end', 'mall_name']
    list_per_page = 10
    ordering = ['lease_start', 'lease_end']
    list_select_related = ['mall']
    search_fields = ['name__istartswith', 'mall__name__istartswith']
    list_filter = ['lease_start', 'lease_end']
    autocomplete_fields = ['mall']
    readonly_fields = ['lease_start']

    def mall_name(self, store):
        return store.mall.name


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'store_name', 'mall_name']
    list_per_page = 10
    ordering = ['name']
    list_select_related = ['mall', 'store']
    search_fields = ['name__istartswith', 'phone__istartswith',
                     'store__name__istartswith', 'mall__name__istartswith']
    autocomplete_fields = ['store', 'mall']

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
    search_fields = ['name__istartswith', 'phone__istartswith']
    list_filter = ['last_visit']
