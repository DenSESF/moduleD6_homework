from django_filters import FilterSet
from django_filters import (
    CharFilter,
    # DateFilter,
    ModelChoiceFilter,
    IsoDateTimeFilter,
)
from django import forms
from whiteboard.models import Post, Author


class NewsFilter(FilterSet):
    author = ModelChoiceFilter(
        lookup_expr='exact',
        label='Автор',
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select-sm'})
    )
    header = CharFilter(
        lookup_expr='icontains',
        label='Заголовок содержит',
        widget=forms.TextInput(attrs={'class': 'form-control-sm'})
    )
    # было DateFilter
    time = IsoDateTimeFilter(
        lookup_expr='lt',
        label='Дата позже',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm',
            'type': 'date',
            }
        )
    )

    class Meta():
        model = Post
        fields = ['header', 'time', 'author', ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(type=Post.NEWS)
