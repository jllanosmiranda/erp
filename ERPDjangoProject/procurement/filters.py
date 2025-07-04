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

class SupplierProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "product_name": ["icontains"],
            "code": ["icontains"]
        }
