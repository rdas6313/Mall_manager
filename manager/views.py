from django.shortcuts import render, HttpResponse
from . import models
from math import ceil


def index(request, mall_id):

    table = request.GET.get('table', None)
    page = request.GET.get('page', 1)
    page_size = 2
    current_pages = {'store': 1, 'inventory': 1}
    if table is not None:
        current_pages[table] = int(page)
    store_headers = ('name', 'description', 'lease_start', 'lease_end')

    queryset = models.Store.objects.filter(
        mall=mall_id).values_list(*store_headers)
    store_count = queryset.count()
    store_list = queryset[page_size *
                          (current_pages['store']-1): page_size * current_pages['store']]

    inventory_headers = ('name', 'description', 'quantity')
    queryset = models.Inventory.objects.filter(
        mall=mall_id).values_list(*inventory_headers)
    inventory_list = queryset[page_size *
                              (current_pages['inventory']-1): page_size * (current_pages['inventory'])]
    print(type(page))
    context = {
        'store': {
            'headers': store_headers,
            'rows': store_list,
            'page': {
                'mall': mall_id,
                'pages': [i+1 for i in range(ceil(store_count/page_size))],
                'table': 'store',
                'current_page': int(page)
            }
        },
        'inventory': {
            'headers': inventory_headers,
            'rows': inventory_list
        }
    }
    return render(request, 'manager/index.html', context=context)
