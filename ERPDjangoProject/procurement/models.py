from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=20)
    product_description = models.TextField()

    def __str__(self):
        return self.product.product_name + ' ' + self.supplier.name

class SupplierProductPrice(models.Model):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()

class PurchaseOrder(models.Model):
    purchase_order_number = models.CharField(max_length=20)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField()
    delivery_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.purchase_order_number

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.product_name + ' ' + str(self.quantity)


class Purchase(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.product_name + ' ' + str(self.quantity)
