import django_filters
from django_filters import FilterSet
from .models import Product, Supplier

class ProductFilter(FilterSet):
    product_name = django_filters.CharFilter(lookup_expr='icontains',
                                             label="Nombre de producto")
    code = django_filters.CharFilter(lookup_expr='icontains',
                                     label="Codigo de producto")

    suppliers = django_filters.ModelChoiceFilter(queryset=Supplier.objects.all(),
                                                        label="Proveedores",
                                                         empty_label="----Todos----")
    class Meta:
        model = Product
        fields = ['product_name', 'code', 'suppliers']

    @property
    def has_active_filter(self):
        if not self.is_bound or not self.is_valid():
            return False
        return any(bool(value) for name, value in self.form.cleaned_data.items() if value is not None)

class SupplierFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains',
                                     label="Nombre")
    ruc = django_filters.CharFilter(lookup_expr='icontains',
                                     label="RUC")

    class Meta:
        model = Supplier
        fields = ['name', 'ruc']

    @property
    def has_active_filter(self):
        if not self.is_bound or not self.is_valid():
            return False
        return any(bool(value) for name, value in self.form.cleaned_data.items() if value is not None)


class SupplierProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "product_name": ["icontains"],
            "code": ["icontains"]
        }

    @property
    def has_active_filter(self):
        if not self.is_bound or not self.is_valid():
            return False
        return any(bool(value) for name, value in self.form.cleaned_data.items() if value is not None)
