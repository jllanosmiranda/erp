from django.shortcuts import render, redirect
from .models import Product, Supplier
from .forms import ProductForm, SupplierForm

# Create your views here.
def suppliers(request):
    if request.method == 'POST':
        supplierForm = SupplierForm(request.POST)
        if supplierForm.is_valid():
            supplierForm.save()
            return redirect('suppliers')

    else:
        supplierForm = SupplierForm()

    suppliers = Supplier.objects.all()
    context = {'suppliers': suppliers, 'form': supplierForm}
    return render(request, 'procurement/suppliers.html', context=context)

def products(request):
    if request.method == 'POST':
        productForm = ProductForm(request.POST)
        if productForm.is_valid():
            productForm.save()
            return redirect('products')

    else:
        productForm = ProductForm()

    products = Product.objects.all()
    return render(request, 'procurement/products.html', context={'products': products, 'form': productForm})

def purchase_orders(request):
    return render(request, 'procurement/purchase_orders.html')

def purchases(request):
    return render(request, 'procurement/purchases.html')