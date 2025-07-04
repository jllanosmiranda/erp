from django.db import models

from ..models import PurchaseOrder, Supplier, Product


class GoodReceiptNote(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING)
    number = models.CharField(default="")
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, default="")
    date = models.DateField()


class GoodReceiptNoteItem(models.Model):
    good_receipt_note = models.ForeignKey(GoodReceiptNote, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
