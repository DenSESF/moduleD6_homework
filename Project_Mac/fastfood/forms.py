from django.forms import ModelForm
from .models import Product
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'type', 'description']
        labels = {
            'name': 'Название',
            'price': 'Цена',
            'type': 'Категория',
            'description': 'Описание',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите названи продукта',
            }),
            'price': forms.TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'value': 0,
                'min': 0,
            }),
            'type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }
