from django import forms


class StoreForm(forms.Form):
    name = forms.CharField(max_length=100, initial='', required=True)
    description = forms.CharField(
        max_length=300, widget=forms.Textarea, initial='', required=True)
    lease_end = forms.DateField(input_formats=['%Y-%m-%d'], required=True)
