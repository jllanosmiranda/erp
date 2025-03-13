
from django.forms.models import ModelForm
from django import forms
from .models import Product, Supplier, SupplierProduct, SupplierProductPrice
from django.core.validators import MinValueValidator
from django.forms import inlineformset_factory


class SupplierForm(ModelForm):
    website = forms.URLField(required=False)

    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierProductForm(ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, validators=[MinValueValidator(0)])

    class Meta:
        model = SupplierProduct
        fields = ['supplier', 'price']

    def __init__(self, *args, **kwargs):
        supplier_product = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if supplier_product:
            supplier_product_price = supplier_product.prices.order_by('-effective_date').first()
            self.fields['price'].initial = supplier_product_price.price

    def save(self, commit=True):
        supplier_product = super().save(commit=False)
        supplier_product_price = SupplierProductPrice(price=self.cleaned_data.get('price'))
        supplier_product_price.supplier_product = supplier_product

        if commit:
            supplier_product.save()
            supplier_product_price.save()
            supplier_product.prices.add(supplier_product_price)

class BaseSupplierProductPriceSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        select_suppliert = set()
        for form in self.forms:
            if form.instance.pk:
                select_suppliert.add(form.instance.supplier.pk)
                form.fields['supplier'].disabled = True
            else:
                form.fields['supplier'].queryset = Supplier.objects.exclude(pk__in=select_suppliert)



SupplierProductPriceSet = inlineformset_factory(Product,
                                                SupplierProduct,
                                                form=SupplierProductForm,
                                                formset=BaseSupplierProductPriceSet,
                                                extra=1
                                                )


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'product_description']

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        return product_name.strip().lower()

    def clean_product_description(self):
        product_description = self.cleaned_data.get('product_description')
        return product_description.strip().lower()
