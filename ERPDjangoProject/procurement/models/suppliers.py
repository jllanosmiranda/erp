from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, unique=True, blank=True)
    email = models.EmailField(max_length=100, null=True, unique=True, blank=True)
    website = models.URLField(max_length=200, null=True, unique=True, blank=True)
    ruc = models.CharField(max_length=15, null=True, unique=True, blank=True)

    def __str__(self):
        return self.name


class SupplierContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name="contacts")
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)


class Bank(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=20)


class SupplierBankAccount(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name="bank_account")
    account = models.CharField(max_length=50)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, related_name="suppliers_banks")
