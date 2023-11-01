from django_filters import FilterSet
from django_filters import CharFilter, ChoiceFilter, NumberFilter
#from django.db import models
from django import forms
from .models import Product


# class ProductFilter(FilterSet):
#     class Meta:
#         model = Product
#         # fields = ['name', 'description', 'type', 'price']
#         fields = {
#             'name':['icontains'],
#             'description': ['icontains'],
#             'type': ['exact'],
#             'price': ['lt'],
#         }

class ProductFilter(FilterSet):
    name = CharFilter(
        lookup_expr='icontains',
        label = 'Название содержит',
        widget=forms.TextInput(attrs={'class': 'form-control-sm'})
    )
    description = CharFilter(
        lookup_expr='icontains',
        label='Описание содержит',
        widget=forms.TextInput(attrs={'class': 'form-control-sm'})
    )
    type = ChoiceFilter(
        lookup_expr='exact',
        label='Категория',
        choices = Product.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select-sm'})
    )
    price = NumberFilter(
        lookup_expr='lt',
        label='Цена меньше',
        widget = forms.TextInput(attrs={'class': 'form-control-sm', 'type': 'number', 'min': 0 })
    )

    class Meta():
        model = Product
        fields = ['name', 'description', 'type', 'price']
        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #             'widget': forms.TextInput(attrs={'class': 'form-control-sm'})
        #         },
        #     },
        #     models.IntegerField: {
        #         'filter_class': CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'lt',
        #             'widget': forms.TextInput(attrs={'class': 'form-control-sm', 'type': 'number', 'min': 0 })
        #         },
        #     },
        #     models.TextField: {
        #         'filter_class': CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #             'widget': forms.TextInput(attrs={'class': 'form-control-sm'})
        #         },
        #     },
        # }
