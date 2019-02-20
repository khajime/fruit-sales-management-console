from django import forms
from django.utils import timezone


from . import models


class SaleForm(forms.ModelForm):
    class Meta:
        model = models.Sale
        fields = ('fruit', 'number', 'sold_at')
        widgets = {
            'sold_at': forms.DateTimeInput,
        }
        initial = {
            'fruit': {'required': True},
            'sold_at': {'input_format': '%Y-%m-%d %H:%M'}
        }
