from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm


class StoreForm(forms.Form):
    name = forms.CharField(max_length=100, initial='', required=True)
    description = forms.CharField(
        max_length=300, widget=forms.Textarea, initial='', required=True)
    lease_end = forms.DateField(input_formats=['%Y-%m-%d'], required=True)


class InventoryForm(forms.Form):
    name = forms.CharField(max_length=100, initial='', required=True)
    description = forms.CharField(
        max_length=300, widget=forms.Textarea, initial='', required=True)
    quantity = forms.IntegerField(min_value=1, max_value=1000, initial=0)


class EmployeeForm(forms.Form):
    name = forms.CharField(max_length=100, initial='', required=True)
    phone = forms.CharField(min_length=10, max_length=10,
                            initial='', required=True)
    address = forms.CharField(
        max_length=300, widget=forms.Textarea, initial='', required=True)
    store_id = forms.ChoiceField(
        choices=[], widget=forms.Select(attrs={'class': 'form-select'}), required=False)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['store_id'].choices = choices


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, initial='')
    mall_name = forms.CharField(max_length=100, initial='', required=True)
    mall_address = forms.CharField(
        max_length=300, widget=forms.Textarea, initial='', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = ''
