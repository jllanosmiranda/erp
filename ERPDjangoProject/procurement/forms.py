
from django.forms.models import ModelForm
from django import forms
from .models import Product, Supplier, SupplierProduct, SupplierProductPrice
from django.core.validators import MinValueValidator
from django.forms import inlineformset_factory
import logging

logging.basicConfig(level=logging.DEBUG)


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
        logging.info(args)
        logging.info(kwargs)
        logging.info(self.forms)
        select_suppliert = set()
        logging.info("this is a log")

        for form in self.forms:
            logging.info('forms in the init')
            logging.info(form.fields['supplier'])
            if form.instance.pk:
                select_suppliert.add(form.instance.supplier.pk)
                form.fields['supplier'].widget.attrs['readonly'] = True
                logging.info(form.instance)
            else:
                logging.info(select_suppliert)
                form.fields['supplier'].queryset = Supplier.objects.exclude(pk__in=select_suppliert)

    @property
    def product_instance(self):
        return None

    @product_instance.setter
    def product_instance(self, product_instance):
        for form in self.forms:
            logging.info("forms instance product")
            logging.info(form.instance)
            form.instance.product = product_instance



SupplierProductPriceSet = inlineformset_factory(Product,
                                                SupplierProduct,
                                                form=SupplierProductForm,
                                                formset=BaseSupplierProductPriceSet,
                                                extra=1
                                                )


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'code']

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        return product_name.strip().lower()

    def clean_product_description(self):
        product_description = self.cleaned_data.get('product_description')
        return product_description.strip().lower()
