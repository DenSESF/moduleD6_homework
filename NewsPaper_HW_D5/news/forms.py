from django.forms import ModelForm
from whiteboard.models import Post
from django import forms


class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            # 'type',
            'category',
            'header',
            'text'
            ]
        labels = {
            'author': 'Автор',
            # 'type': 'Тип',
            'category': 'Категория',
            'header': 'Заголовок',
            'text': 'Текст',
            }

        widgets = {
                'author': forms.Select(attrs={
                    'class': 'form-select',
                }),
                # 'type': forms.HiddenInput(),
                # 'type': forms.Select(attrs={
                #     'class': 'form-select',
                # }),
                'category': forms.SelectMultiple(attrs={
                    'class': 'form-select',
                }),
                'header': forms.TextInput(attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'maxlength': 255,
                }),
                'text': forms.Textarea(attrs={
                    'class': 'form-control',
                }),
            }
