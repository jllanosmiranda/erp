from django.db import models
from django.utils.timezone import now

from ..models import Supplier, Product
from ..models.constants import CURRENCY_CHOICES, UNIT_OF_MEASURE_CHOICES
from main.models import EntityBaseModel, EventBaseModel


class SupplierProduct(EntityBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_product")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="supplier_product")
    product_code = models.CharField(max_length=20)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.IntegerField(choices=CURRENCY_CHOICES)
    unit_of_measure = models.CharField(max_length=50, blank=True, default='', choices=UNIT_OF_MEASURE_CHOICES)

    def __str__(self):
        return self.product.product_name


class SupplierProductEvent(EventBaseModel):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, related_name="prices")
