from django.db import models
from django.contrib.auth.models import User

from ..models import SupplierProduct, Product, Supplier
from ..models.constants import CURRENCY_CHOICES, UNIT_OF_MEASURE_CHOICES
from main.models import EntityBaseModel, EventBaseModel


class PurchaseRequirement(EntityBaseModel):
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
    status = models.IntegerField(choices=status_choices)
    payment_condition = models.IntegerField(choices=payment_condition, default=0)
    shipping_condition = models.TextField(default="", blank=True)
    comments = models.TextField(default="", blank=True)

    @property
    def date(self):
        print(self.created_at)
        return self.created_at.strftime("%d/%m/%Y")


class PurchaseRequirementItems(EntityBaseModel):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.DO_NOTHING)
    purchase_requirement = models.ForeignKey(PurchaseRequirement, on_delete=models.DO_NOTHING, related_name="items")
    quantity = models.IntegerField()
    price = models.FloatField()
    currency = models.IntegerField(choices=CURRENCY_CHOICES)
    unit_of_measure = models.CharField(max_length=50, blank=True, default='', choices=[('', '---------')] + UNIT_OF_MEASURE_CHOICES)
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


class PurchaseRequirementEvent(EventBaseModel):
    purchase_requirement = models.ForeignKey(PurchaseRequirement, on_delete=models.CASCADE, related_name="events")

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, purchase_requirement=instance, **kwargs)


class PurchaseRequirementItemEvent(EventBaseModel):
    purchase_requirement_item = models.ForeignKey(PurchaseRequirementItems, on_delete=models.CASCADE, related_name="events")

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, purchase_requirement_item=instance, **kwargs)

