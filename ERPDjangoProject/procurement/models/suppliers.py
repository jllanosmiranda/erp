from django.db import models
from main.models import EntityBaseModel, EventBaseModel


class Supplier(EntityBaseModel):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, unique=True, blank=True)
    email = models.EmailField(max_length=100, null=True, unique=True, blank=True)
    website = models.URLField(max_length=200, null=True, unique=True, blank=True)
    ruc = models.CharField(max_length=15, null=True, unique=True, blank=True)

    def __str__(self):
        return self.name


class SupplierContact(EntityBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name="contacts")
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, blank=True, default="")
    email = models.EmailField(max_length=100, blank=True, default="")


class Bank(EntityBaseModel):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=20)


class SupplierBankAccount(EntityBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name="bank_account")
    account = models.CharField(max_length=50)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, related_name="suppliers_banks")


class SupplierEvent(EventBaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="events")

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, supplier=instance, **kwargs)
