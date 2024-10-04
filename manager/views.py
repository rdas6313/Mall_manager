from django.shortcuts import render, HttpResponse
from django.http.response import Http404
from . import models
from math import ceil
from django.db.models import F
from django.db import IntegrityError
from .forms import StoreForm


def get_store_data(current_pages, page_size, mall_id):
    store_headers = ('name', 'description', 'lease_start', 'lease_end')

    queryset = models.Store.objects.filter(
        mall=mall_id).order_by('-id')
    store_count = queryset.count()
    store_list = queryset[page_size *
                          (current_pages['store']-1): page_size * current_pages['store']]

    return (store_headers, store_list, store_count)


def index(request, mall_id):

    table = request.GET.get('table', None)
    page = request.GET.get('page', 1)
    page_size = 2
    current_pages = {'store': 1, 'inventory': 1, 'employee': 1, 'customer': 1}
    if table is not None and table in current_pages:
        current_pages[table] = int(page)

    store_headers, store_list, store_count = get_store_data(
        current_pages, page_size, mall_id)
    store_list = store_list.values_list(*store_headers)

    inventory_headers = ('name', 'description', 'quantity')
    queryset = models.Inventory.objects.filter(
        mall=mall_id).values_list(*inventory_headers)
    inventory_count = queryset.count()
    inventory_list = queryset[page_size *
                              (current_pages['inventory']-1): page_size * (current_pages['inventory'])]

    emp_headers = ['name', 'phone', 'address', 'store']
    employee_headers = ('name', 'phone', 'address', 'store__name')

    queryset = models.Employee.objects.filter(
        mall=mall_id).select_related('store').values_list(*employee_headers)
    employee_list = queryset[page_size *
                             (current_pages['employee']-1): page_size * (current_pages['employee'])]
    employee_count = queryset.count()

    customer_headers = ('name', 'phone', 'address', 'last_visit')
    queryset = models.Customer.objects.filter(
        mall=mall_id).values_list(*customer_headers)
    customer_count = queryset.count()
    customer_list = queryset[page_size *
                             (current_pages['customer']-1): page_size * (current_pages['customer'])]
    print(customer_list)
    context = {
        'store': {
            'headers': store_headers,
            'rows': store_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(store_count/page_size))],
                'table': 'store',
                'current_page': current_pages['store'],
                'url_name': 'index'
            }
        },
        'inventory': {
            'headers': inventory_headers,
            'rows': inventory_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(inventory_count/page_size))],
                'table': 'inventory',
                'current_page': current_pages['inventory'],
                'url_name': 'index'
            }
        },
        'employee': {
            'headers': emp_headers,
            'rows': employee_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(employee_count/page_size))],
                'table': 'employee',
                'current_page': current_pages['employee'],
                'url_name': 'index'
            }
        },
        'customer': {
            'headers': customer_headers,
            'rows': customer_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(customer_count/page_size))],
                'table': 'customer',
                'current_page': current_pages['customer'],
                'url_name': 'index'
            }
        }
    }
    return render(request, 'manager/index.html', context=context)


def create_store(request, mall_id, store_id=None, is_update=1):
    msg = None
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            lease_end = form.cleaned_data['lease_end']
            try:
                models.Store.objects.create(
                    name=name, description=description, lease_end=lease_end, mall_id=mall_id)
                msg = 'Successfully created new store!'
                form = StoreForm()
            except IntegrityError:
                msg = 'Unable to create new store due to error!'

    else:
        form = StoreForm()

    table = request.GET.get('table', 'store')
    page = request.GET.get('page', 1)
    page_size = 2
    current_pages = {'store': 1}
    if table is not None and table in current_pages:
        current_pages[table] = int(page)

    store_headers, store_list, store_count = get_store_data(
        current_pages, page_size, mall_id)

    store_headers = (*store_headers, 'action')
    store_list = store_list.annotate(
        action=F('id')).values_list(*store_headers)

    context = {
        'form_title': 'Add Store',
        'form_type': 'store',
        'form': form,
        'form_status_msg': msg,
        'store': {
            'headers': store_headers,
            'rows': store_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(store_count/page_size))],
                'table': 'store',
                'current_page': current_pages['store'],
                'url_name': 'create_store'
            }
        }
    }
    return render(request, 'manager/edit.html', context=context)
