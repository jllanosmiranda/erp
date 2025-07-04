from django.db import models

from .suppliers import Supplier


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_description = models.TextField()
    suppliers = models.ManyToManyField(Supplier, through="SupplierProduct", related_name="products")
    code = models.CharField(default='')

    def __str__(self):
        return self.product_name
