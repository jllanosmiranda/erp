from django.db import models
from django.utils.timezone import now

from ..models import Supplier, Product


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
        return price_obj.price if price_obj else None


class SupplierProductPrice(models.Model):
    CURRENCY_CHOICES = [
        ('soles', 'Soles'),
        ('dolares', 'Dólares'),
    ]
    
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='soles')
    effective_date = models.DateTimeField(default=now)
