from django.db import models
from django.contrib.auth.models import User

from ..models import SupplierProduct, Product, Supplier
from ..models.constants import CURRENCY_CHOICES


class PurchaseRequirement(models.Model):
    status_choices = [
        (0, 'pending'),
        (1, 'approved'),
        (2, 'rejected')
    ]
    payment_condition = [
        (0, 'al contado'),
        (1, 'credito'),
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateField(auto_now=True)
    status = models.IntegerField(choices=status_choices)
    payment_condition = models.IntegerField(choices=payment_condition, default=0)
    shipping_condition = models.TextField(default="", blank=True)
    comments = models.TextField(default="", blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")


class PurchaseRequirementItems(models.Model):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.DO_NOTHING)
    purchase_requirement = models.ForeignKey(PurchaseRequirement, on_delete=models.DO_NOTHING, related_name="items")
    quantity = models.IntegerField()
    price = models.FloatField()
    currency = models.IntegerField(choices=CURRENCY_CHOICES)
    def __str__(self):
        return self.supplier_product.product.product_name

    @property
    def subtotal(self):
        return self.quantity * self.price


class PurchaseOrder(models.Model):
    purchase_order_number = models.IntegerField()
    delivery_date = models.DateField()


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.IntegerField(choices=CURRENCY_CHOICES, default=0)

    def __str__(self):
        return self.product.product_name + ' ' + str(self.quantity)


class PurchaseInvoice(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING)


