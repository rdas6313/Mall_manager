from django.shortcuts import redirect, render, HttpResponse
from django.http.response import Http404
from . import models
from math import ceil
from django.db.models import F
from django.db import IntegrityError, transaction
from django.urls import reverse
from .forms import StoreForm, InventoryForm, EmployeeForm


PAGE_SIZE = 4


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
    page_size = PAGE_SIZE
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
    msg = request.GET.get('msg', msg)
    page_size = PAGE_SIZE
    current_pages = {'store': 1}
    if table is not None and table in current_pages:
        current_pages[table] = int(page)

    store_headers, store_list, store_count = get_store_data(
        current_pages, page_size, mall_id)

    store_headers = (*store_headers, 'action')
    store_list = store_list.annotate(
        action=F('id')).values_list(*store_headers)

    form_url = reverse('create_store', args=[mall_id])
    back_url = reverse('index', args=[mall_id])

    context = {
        'form_title': 'Add Store',
        'form_type': 'store',
        'form': form,
        'form_status_msg': msg,
        'form_url': form_url,
        'back_url': back_url,
        'form_template': 'manager/add_store.html',
        'list_data': {
            'update_url_name': 'update_store',
            'delete_url_name': 'delete_store',
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


def update_store(request, mall_id, store_id):
    msg = None
    form = None

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():

            row = models.Store.objects.filter(pk=store_id) \
                .update(name=form.cleaned_data['name'],
                        description=form.cleaned_data['description'],
                        lease_end=form.cleaned_data['lease_end'])
            if row > 0:
                msg = 'updated successfully!'
            else:
                msg = 'Updation not happended,(Could be invalid store id)!'
            url = reverse('create_store', args=[mall_id])
            url += '?msg=' + msg
            return redirect(url)

    else:
        store = models.Store.objects.filter(pk=store_id).values()
        if store:
            store = store[0]
        else:
            raise Http404('Wrong store!')
        form = StoreForm(store)

    form_url = reverse('update_store', args=[mall_id, store_id])
    back_url = reverse('create_store', args=[mall_id])
    context = {
        'form_title': 'Update Store',
        'form_type': 'store',
        'form': form,
        'form_status_msg': msg,
        'form_url': form_url,
        'back_url': back_url,
        'form_template': 'manager/add_store.html',
    }
    return render(request, 'manager/edit.html', context=context)


def delete_store(request, mall_id, store_id):
    row = models.Store.objects.filter(pk=store_id).delete()
    if row[0] > 0:
        msg = "Successfully Deleted!"
    else:
        msg = "Unable to delete!"
    url = reverse('create_store', args=[mall_id])
    url += '?msg=' + msg
    return redirect(url)


def create_inventory(request, mall_id):
    msg = None
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            quantity = form.cleaned_data['quantity']
            try:
                with transaction.atomic():
                    inventory = models.Inventory.objects.create(
                        name=name, description=description, quantity=quantity)
                    mall = models.Mall.objects.get(pk=mall_id)
                    mall.inventories.add(inventory)
                msg = 'Successfully created new inventory item!'
                form = InventoryForm()
            except IntegrityError:
                msg = 'Unable to create new inventory item due to error!'
            except models.Mall.DoesNotExist:
                msg = 'Unable to create new inventory item due to invalid mall id!'
            except Exception as e:
                msg = f'unknown error {e}'

    else:
        form = InventoryForm()

    page = request.GET.get('page', 1)
    msg = request.GET.get('msg', msg)
    page_size = PAGE_SIZE
    current_pages = int(page)
    store_headers = ('name', 'description', 'quantity', 'action')
    queryset = models.Inventory.objects.filter(
        mall=mall_id).annotate(action=F('id')).order_by('-id').values_list(*store_headers)
    store_count = queryset.count()
    store_list = queryset[page_size *
                          (current_pages-1): page_size * current_pages]

    form_url = reverse('create_inventory', args=[mall_id])
    back_url = reverse('index', args=[mall_id])

    context = {
        'form_title': 'Add Inventory',
        'form': form,
        'form_status_msg': msg,
        'form_url': form_url,
        'back_url': back_url,
        'form_template': 'manager/add_inventory.html',
        'list_data': {
            'update_url_name': 'update_inventory',
            'delete_url_name': 'delete_inventory',
            'headers': store_headers,
            'rows': store_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(store_count/page_size))],
                'table': 'inventory',
                'current_page': current_pages,
                'url_name': 'create_inventory'
            }
        }
    }
    return render(request, 'manager/edit.html', context=context)


def update_inventory(request, mall_id, inventory_id):
    msg = None
    form = None

    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():

            row = models.Inventory.objects.filter(pk=inventory_id) \
                .update(name=form.cleaned_data['name'],
                        description=form.cleaned_data['description'],
                        quantity=form.cleaned_data['quantity'])
            if row > 0:
                msg = 'updated successfully!'
            else:
                msg = 'Updation not happended due to may be invalid inventory id!'
            url = reverse('create_inventory', args=[mall_id])
            url += '?msg=' + msg
            return redirect(url)

    else:
        inventory = models.Inventory.objects.filter(pk=inventory_id).values()
        if inventory:
            inventory = inventory[0]
        else:
            raise Http404('Wrong inventory!')
        form = InventoryForm(inventory)

    form_url = reverse('update_inventory', args=[mall_id, inventory_id])
    back_url = reverse('create_inventory', args=[mall_id])
    context = {
        'form_title': 'Update Inventory',
        'form_type': 'store',
        'form': form,
        'form_status_msg': msg,
        'form_url': form_url,
        'back_url': back_url,
        'form_template': 'manager/add_inventory.html',
    }
    return render(request, 'manager/edit.html', context=context)


def delete_inventory(request, mall_id, inventory_id):
    row = models.Inventory.objects.filter(pk=inventory_id).delete()
    if row[0] > 0:
        msg = "Successfully Deleted!"
    else:
        msg = "Unable to delete!"
    url = reverse('create_inventory', args=[mall_id])
    url += '?msg=' + msg
    return redirect(url)


def create_employee(request, mall_id):
    choices = [(None, 'None')] + [(store.id, store.name)
                                  for store in models.Store.objects.filter(mall=mall_id).all().distinct()]
    if request.method == 'POST':
        form = EmployeeForm(request.POST, choices=choices)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            store_id = form.cleaned_data.get('store_id', None)
            try:
                models.Employee.objects.create(
                    name=name, phone=phone, address=address, store_id=store_id, mall_id=mall_id)
                form = EmployeeForm(choices=choices)
                msg = "Employee created successfully!"
            except IntegrityError:
                msg = "Error: Unable to create employee!"
    else:
        form = EmployeeForm(choices=choices)

    page_size = PAGE_SIZE
    msg = request.GET.get('msg', None)
    current_page = int(request.GET.get('page', 1))
    employee_headers = ('name', 'phone', 'address',
                        'store_name', 'action')
    queryset = models.Employee.objects.filter(mall=mall_id).annotate(
        store_name=F('store__name'), action=F('id')).order_by('-id').values_list(*employee_headers)
    employee_count = queryset.count()
    employee_list = queryset[page_size *
                             (current_page-1): page_size * current_page]

    form_url = reverse('create_employee', args=[mall_id])
    back_url = reverse('index', args=[mall_id])

    context = {
        'form_title': 'Add Employee',
        'form': form,
        'form_status_msg': msg,
        'form_url': form_url,
        'back_url': back_url,
        'form_template': 'manager/add_employee.html',
        'list_data': {
            'update_url_name': 'update_employee',
            'delete_url_name': 'delete_employee',
            'headers': employee_headers,
            'rows': employee_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(employee_count/page_size))],
                'table': 'None',
                'current_page': current_page,
                'url_name': 'create_employee'
            }
        }

    }
    return render(request, 'manager/edit.html', context=context)


def update_employee(request, mall_id, emp_id):
    msg = None
    choices = [(None, 'None')] + [(store.id, store.name)
                                  for store in models.Store.objects.filter(mall=mall_id).all().distinct()]
    if request.method == "POST":
        form = EmployeeForm(request.POST, choices=choices)
        if form.is_valid():
            row = models.Employee.objects.filter(pk=emp_id).update(name=form.cleaned_data['name'], phone=form.cleaned_data['phone'],
                                                                   address=form.cleaned_data['address'],
                                                                   store_id=form.cleaned_data['store_id'])
            if row > 0:
                msg = 'updated successfully!'
            else:
                msg = 'Updation not happended due to may be invalid employee id!'
            url = reverse('create_employee', args=[mall_id])
            url += '?msg=' + msg
            return redirect(url)
    else:
        emp = models.Employee.objects.filter(
            pk=emp_id).values()
        emp = emp[0] if emp else None
        form = EmployeeForm(emp, choices=choices)

    form_url = reverse('update_employee', args=[mall_id, emp_id])
    back_url = reverse('create_employee', args=[mall_id])
    context = {
        'form_title': 'Update Employee',
        'form_type': 'store',
        'form': form,
        'form_status_msg': msg,
        'form_url': form_url,
        'back_url': back_url,
        'form_template': 'manager/add_employee.html',
    }
    return render(request, 'manager/edit.html', context=context)


def delete_employee(request, mall_id, emp_id):
    row = models.Employee.objects.filter(pk=emp_id).delete()
    if row[0] > 0:
        msg = "Successfully Deleted!"
    else:
        msg = "Unable to delete!"
    url = reverse('create_employee', args=[mall_id])
    url += '?msg=' + msg
    return redirect(url)
