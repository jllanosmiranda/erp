
from django.forms.models import ModelForm
from django import forms
from .models import Product, Supplier


class SupplierForm(ModelForm):
    website = forms.URLField(required=False)

    class Meta:
        model = Supplier
        fields = '__all__'



class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'