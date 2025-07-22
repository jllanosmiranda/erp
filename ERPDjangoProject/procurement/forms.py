
from django.forms.models import ModelForm
from django import forms
from .models import Product, Supplier, SupplierProduct, SupplierProductPrice, SupplierContact, SupplierBankAccount, \
    GoodReceiptNote, GoodReceiptNoteItem
from django.core.validators import MinValueValidator, RegexValidator
from django.forms import inlineformset_factory
import logging

logging.basicConfig(level=logging.DEBUG)


class SupplierForm(ModelForm):
    website = forms.URLField(required=False,
                             label="Sitio Web")
    address = forms.CharField(required=False,
                              label="Direccion",)
    phone = forms.CharField(required=False,
                            label="Telefono")
    email = forms.EmailField(required=False,
                             label="Email")
    ruc = forms.CharField(required=False,
                          max_length=15,
                          validators=[
                              RegexValidator(regex=r'^[0-9]+$',
                                             message='RUC debe de ser un numero')
                          ],
                          label="RUC")

    class Meta:
        model = Supplier
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields(['name', 'ruc', 'address', 'phone', 'email', 'website'])
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['class'] = 'supplier-field'

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if not website:
            return None
        return website


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

        return supplier_product




SupplierProductPriceSet = inlineformset_factory(Product,
                                                SupplierProduct,
                                                form=SupplierProductForm,
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


class SupplierContactForm(ModelForm):
    class Meta:
        model = SupplierContact
        fields = '__all__'

class BaseSupplierContactSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def instance(self):
        return None

    @instance.setter
    def instance(self, instance):
        if instance:
            for form in self.forms:
                form.instance = instance

SupplierContactSet = inlineformset_factory(Supplier,
                                           SupplierContact,
                                           form=SupplierContactForm,
                                           extra=1)

class SupplierBankForm(ModelForm):
    class Meta:
        model = SupplierBankAccount
        fields = '__all__'


class BaseSupplierBankSet(forms.BaseModelFormSet):
    @property
    def instance(self):
        return None

    @instance.setter
    def instance(self, instance):
        if instance:
            for form in self.forms:
                form.instance = instance

SupplierBankSet = inlineformset_factory(Supplier,
                                        SupplierBankAccount,
                                        form=SupplierBankForm,
                                        extra=1)

class GoodReceiptNoteForm(ModelForm):
    class Meta:
        model = GoodReceiptNote
        fields = '__all__'

        widgets = {"date": forms.DateInput(attrs={'type': 'date'}),
                   "supplier": forms.Select(attrs={'class': 'form-control'})}


class GoodReceiptNoteItemForm(ModelForm):
    class Meta:
        model = GoodReceiptNoteItem
        fields = ['product', 'quantity']


class BaseGoodReceiptNoteItemFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, supplier_id, **kwargs):

        super().__init__(*args, **kwargs)
        supplier = Supplier.objects.get(id=supplier_id)
        products = supplier.products.all()

        for form in self.forms:
            form.fields['product'].queryset = products

def form_set(extra):

    GoodReceiptNoteItemSet = inlineformset_factory(GoodReceiptNote,
                                                   GoodReceiptNoteItem,
                                                   form=GoodReceiptNoteItemForm,
                                                   formset=BaseGoodReceiptNoteItemFormSet,
                                                   can_delete=False,
                                                   extra=extra)

    return GoodReceiptNoteItemSet


class ProductSupplierForm(ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, validators=[MinValueValidator(0)])

    class Meta:
        model = SupplierProduct
        fields = ['product', 'price']

    def __init__(self, *args, **kwargs):
        supplier_product = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if supplier_product:
            supplier_product_price = supplier_product.prices.order_by('-effective_date').first()
            self.fields['price'].initial = supplier_product_price.price
            self.fields['product'].initial = supplier_product.product

    def save(self, commit=True):
        supplier_product = super().save(commit=False)
        price = self.cleaned_data.get('price')
        logging.info(f"price {price}")
        supplier_product_price = SupplierProductPrice(price=price)
        supplier_product_price.supplier_product = supplier_product

        if commit:
            supplier_product.save()
            supplier_product_price.save()
        return supplier_product

class ProductSupplierPriceFormBase(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            products = self.instance.products.all()

            for form in self.forms:
                if not form.instance.pk:
                    form.fields['product'].queryset = Product.objects.exclude(id__in=products)


ProductSupplierFormSet = inlineformset_factory(Supplier,
                                               SupplierProduct,
                                               form=ProductSupplierForm,
                                               formset=ProductSupplierPriceFormBase,
                                               can_delete=True,
                                               extra=1)
