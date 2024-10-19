from django.contrib import admin


class QuantityFilter(admin.SimpleListFilter):
    title = 'Quantity'
    parameter_name = 'quantity'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Less than 10'),
            ('<50', 'Less than 50')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(quantity__lt=10)
        elif self.value() == '<50':
            return queryset.filter(quantity__lt=50)
