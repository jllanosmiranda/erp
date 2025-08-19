from random import choices

from django.db import models
from django.contrib.auth.models import User

from .suppliers import Supplier
from datetime import datetime
from main.models import EntityBaseModel, EventBaseModel


class Product(EntityBaseModel):
    product_name = models.CharField(max_length=200, unique=True)
    product_description = models.TextField(blank=True, null=True)
    suppliers = models.ManyToManyField(Supplier, through="SupplierProduct", related_name="products")
    code = models.CharField(default='', null=True, blank=True, max_length=20)

    def __str__(self):
        return self.product_name


class ProductEvents(EventBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="events")


