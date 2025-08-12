from django.forms.models import ModelForm
from django import forms
from .models import Product, Supplier, SupplierProduct, SupplierProductPrice, SupplierContact, SupplierBankAccount, \
    GoodReceiptNote, GoodReceiptNoteItem, PurchaseRequirement, PurchaseRequirementItems
from django.core.validators import MinValueValidator, RegexValidator
from django.forms import inlineformset_factory
import logging
from .models.constants import CURRENCY_CHOICES

logging.basicConfig(level=logging.DEBUG)


class SupplierForm(ModelForm):
    website = forms.URLField(required=False,
                             label="Sitio Web",
                             widget=forms.URLInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False,
                              label="Direccion",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False,
                            label="Telefono",
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False,
                             label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ruc = forms.CharField(required=False,
                          max_length=15,
                          validators=[
                              RegexValidator(regex=r'^[0-9]+$',
                                             message='RUC debe de ser un numero')
                          ],
                          label="RUC",
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(required=False,
                           label="Nombre",
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )

    class Meta:
        model = Supplier
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields(['name', 'ruc', 'address', 'phone', 'email', 'website'])

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if not website:
            return None
        return website

    def set_fields_readonly(self):
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True

    def unset_fields_readonly(self):
        for field in self.fields.values():
            field.widget.attrs['readonly'] = False


class SupplierProductForm(ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True, validators=[MinValueValidator(0)])
    currency = forms.ChoiceField(choices=[('', '---------')] + CURRENCY_CHOICES, label="Moneda")

    class Meta:
        model = SupplierProduct
        fields = ['supplier', 'price', 'currency']

    def __init__(self, *args, **kwargs):
        supplier_product = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if supplier_product:
            supplier_product_price = supplier_product.prices.order_by('-effective_date').first()
            if supplier_product_price:
                self.fields['price'].initial = supplier_product_price.price
                self.fields['currency'].initial = supplier_product_price.currency

    def save(self, commit=True):
        supplier_product = super().save(commit=False)
        supplier_product_price = SupplierProductPrice(
            price=self.cleaned_data.get('price'),
            currency=self.cleaned_data.get('currency')
        )
        supplier_product_price.supplier_product = supplier_product

        if commit:
            supplier_product.save()
            supplier_product_price.save()
            supplier_product.prices.add(supplier_product_price)

        return supplier_product

class BaseSupplierProductPriceSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def forms_with_data(self):
        logging.info(f"forms with data {self.forms}")
        return [form for form in self.forms if form.instance.pk]

    @property
    def forms_extra(self):
        return [form for form in self.forms if form.instance.pk is None]



SupplierProductPriceSet = inlineformset_factory(Product,
                                                SupplierProduct,
                                                form=SupplierProductForm,
                                                formset=BaseSupplierProductPriceSet,
                                                extra=1
                                                )


class ProductForm(ModelForm):
    product_name = forms.CharField(max_length=200,
                                   label="Nombre",
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                                          label="Descripcion")
    code = forms.CharField(required=False,
                           label="Codigo",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

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
    name = forms.CharField(max_length=50,
                           label="Nombre")
    phone = forms.CharField(max_length=10,
                            required=False,
                            label="Telefono")
    email = forms.EmailField(max_length=100, required=False,
                             label="Email")
    class Meta:
        model = SupplierContact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['class'] = "supplier-contact-field"

    @property
    def get_visible_fields(self):
        return [self['name'],
                self['email'],
                self['phone']]

class BaseSupplierContactSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def forms_with_data(self):
        logging.info(f"forms with data {self.forms}")
        return [form for form in self.forms if form.instance.pk]

    @property
    def forms_extra(self):
        return [form for form in self.forms if form.instance.pk is None]

SupplierContactSet = inlineformset_factory(Supplier,
                                           SupplierContact,
                                           form=SupplierContactForm,
                                           formset=BaseSupplierContactSet,
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
    currency = forms.ChoiceField(choices=[('','----------')] + CURRENCY_CHOICES, label="Moneda")

    class Meta:
        model = SupplierProduct
        fields = ['product', 'price', 'currency']

    def __init__(self, *args, **kwargs):
        supplier_product = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if supplier_product:
            supplier_product_price = supplier_product.prices.order_by('-effective_date').first()
            if supplier_product_price:
                self.fields['price'].initial = supplier_product_price.price
                self.fields['currency'].initial = supplier_product_price.currency
            self.fields['product'].initial = supplier_product.product

    def save(self, commit=True):
        supplier_product = super().save(commit=False)
        price = self.cleaned_data.get('price')
        currency = self.cleaned_data.get('currency')
        logging.info(f"price {price}")
        supplier_product_price = SupplierProductPrice(price=price, currency=currency)
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

    @property
    def forms_with_data(self):
        return [form for form in self.forms if form.instance.pk]

    @property
    def forms_extra(self):
        return [form for form in self.forms if not form.instance.pk]


ProductSupplierFormSet = inlineformset_factory(Supplier,
                                               SupplierProduct,
                                               form=ProductSupplierForm,
                                               formset=ProductSupplierPriceFormBase,
                                               can_delete=True,
                                               extra=1)

class SupplierAddProductForm(forms.ModelForm):
    product_name = forms.CharField(max_length=200)
    product_description = forms.CharField(widget=forms.Textarea)
    code = forms.CharField(required=False)
    price = forms.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES, initial='soles', label="Moneda")

    class Meta:
        model = SupplierProduct
        fields = ['product_name', 'product_description', 'code', 'price', 'currency']  # We'll handle the fields manually

    def __init__(self, *args, supplier=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.supplier = supplier

        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['class'] = 'new-product-field'

    def save(self, commit=True):
        # Create the product first
        product = Product.objects.create(
            product_name=self.cleaned_data['product_name'],
            product_description=self.cleaned_data['product_description'],
            code=self.cleaned_data['code']
        )

        # Create the supplier product relationship
        supplier_product = super().save(commit=False)
        supplier_product.supplier = self.supplier
        supplier_product.product = product
        
        if commit:
            supplier_product.save()
            # Create the price
            SupplierProductPrice.objects.create(
                supplier_product=supplier_product,
                price=self.cleaned_data['price'],
                currency=self.cleaned_data['currency']
            )

        return supplier_product


class PurchaseRequirementForm(ModelForm):
    class Meta:
        model = PurchaseRequirement
        fields = ['date', 'status', 'payment_condition', 'comments', 'shipping_condition']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'shipping_condition': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'date': 'Fecha',
            'status': 'Estado',
            'payment_condition': 'Condicion de pago',
            'comments': 'Observaciones:',
            'shipping_condition': 'Condicion de envio:'
        }


class PurchaseRequirementItemsForm(ModelForm):
    class Meta:
        model = PurchaseRequirementItems
        fields = ['supplier_product', 'quantity', 'price', 'currency']
        labels = {
            'supplier_product': 'Producto',
            'quantity': 'Cantidad',
            'price': 'Precio',
            'currency': 'Moneda'
        }
    
    def __init__(self, *args, supplier=None, **kwargs):
        super().__init__(*args, **kwargs)
        if supplier:
            self.fields['supplier_product'].queryset = SupplierProduct.objects.filter(supplier=supplier)
        
        # Add CSS classes
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['supplier_product'].widget.attrs['class'] += ' supplier-product-selector'
        self.fields['price'].widget.attrs['class'] += ' price-field'
        self.fields['quantity'].widget.attrs['class'] += ' quantity-field'
        self.fields['currency'].widget.attrs['class'] += ' currency-field'


class BasePurchaseRequirementItemsFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, supplier=None, **kwargs):
        self.supplier = supplier
        super().__init__(*args, **kwargs)
        
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['supplier'] = self.supplier
        return kwargs
        
    @property
    def forms_with_data(self):
        return [form for form in self.forms if form.instance.pk]
        
    @property
    def forms_extra(self):
        return [form for form in self.forms if not form.instance.pk]
        
    def calculate_total(self):
        total = 0
        for form in self.forms:
            if form.is_valid() and form.cleaned_data.get('DELETE', False) is False:
                price = form.cleaned_data.get('price', 0)
                quantity = form.cleaned_data.get('quantity', 0)
                total += price * quantity
        return total


def purchase_requirement_items_formset(extra=10):
    return inlineformset_factory(
        PurchaseRequirement,
        PurchaseRequirementItems,
        form=PurchaseRequirementItemsForm,
        formset=BasePurchaseRequirementItemsFormSet,
        extra=extra,
        can_delete=True
    )