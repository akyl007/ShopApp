from PIL.Image import Image
from django.forms import ModelForm, TextInput, ClearableFileInput ,NumberInput, Textarea

from .models import Product, Category


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control',
                                     'placeholder': 'Введите название продукта'}),
            'price': NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'Цена продукта'}),
            'description':Textarea(attrs={'class': 'form-control',
                                          'rows': 4, 'cols': 40,'style': 'resize: none',
                                          'placeholder': ' Описание'}),
            'image': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control',
                                     'placeholder': 'Введите название категории'}),
            'image': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }