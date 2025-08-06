from django.db import models
from django.utils.timezone import now

from ..models import Supplier, Product
from ..models.constants import CURRENCY_CHOICES


class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_product")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="supplier_product")
    product_code = models.CharField(max_length=20)
    product_description = models.TextField()

    def __str__(self):
        return self.product.product_name + ' ' + self.supplier.name

    @property
    def latest_price(self):
        price_obj = self.prices.order_by('-effective_date').first()
        return price_obj


class SupplierProductPrice(models.Model):

    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.IntegerField(choices=CURRENCY_CHOICES)
    effective_date = models.DateTimeField(default=now)
