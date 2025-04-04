from django.db import models
from django.utils.timezone import now

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True, unique=True)
    email = models.EmailField(max_length=100, null=True, unique=True)
    website = models.URLField(max_length=200, null=True, unique=True)
    ruc = models.CharField(max_length=15, null=True, unique=True)

    def __str__(self):
        return self.name

class SupplierContact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name="contacts")
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)

class Bank(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=20)

class SupplierBankAccount(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name="bank_account")
    account = models.CharField(max_length=50)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, related_name="suppliers_banks")


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_description = models.TextField()
    suppliers = models.ManyToManyField(Supplier, through="SupplierProduct", related_name="products")
    code = models.CharField(default='')

    def __str__(self):
        return self.product_name

class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_product")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="supplier_product")
    product_code = models.CharField(max_length=20)
    product_description = models.TextField()

    def __str__(self):
        return self.product.product_name + ' ' + self.supplier.name

class SupplierProductPrice(models.Model):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField(default=now)


CURRENCY_CHOICES = [
    (0, 'usd'),
    (1, 'soles')
]

class PurchaseRequirement(models.Model):
    status_choices = [
        (0, 'pending'),
        (1, 'approved'),
        (2, 'rejected')
    ]
    description = models.TextField()
    date = models.DateField()
    status = models.IntegerField(choices=status_choices)


class PurchaseRequirementItems(models.Model):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.DO_NOTHING)
    purchase_requirement = models.ForeignKey(PurchaseRequirement, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()
    currency = models.IntegerField(choices=CURRENCY_CHOICES)


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

class GoodReceiptNote(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING)
    number = models.CharField(default="")
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, default="")
    date = models.DateField()

class GoodReceiptNoteItem(models.Model):
    good_receipt_note = models.ForeignKey(GoodReceiptNote, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()




