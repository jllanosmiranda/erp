from django_filters import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "product_name": ["icontains"],
            "suppliers": ["exact"],
            "code": ["icontains"]
        }

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
