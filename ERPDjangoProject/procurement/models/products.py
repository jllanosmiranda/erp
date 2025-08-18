from django.db import models

from .suppliers import Supplier
from .constants import UNIT_OF_MEASURE_CHOICES


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_description = models.TextField()
    suppliers = models.ManyToManyField(Supplier, through="SupplierProduct", related_name="products")
    code = models.CharField(default='')
    unit_of_measure = models.CharField(max_length=50, blank=True, default='', choices=UNIT_OF_MEASURE_CHOICES)

    def __str__(self):
        return self.product_name
