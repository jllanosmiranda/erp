from django.shortcuts import render, redirect
from .models import Product, Supplier, SupplierProductPrice
from .forms import ProductForm, SupplierForm, SupplierProductPriceSet
from .filters import ProductFilter

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
    product_filter = ProductFilter(request.GET,
                                    queryset=products)
    print(products)
    print(product_filter.qs)

    context = {'products': product_filter.qs,
               'form': productForm,
               'filter': product_filter}

    return render(request, 'procurement/products.html', context=context)

def new_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        formset = SupplierProductPriceSet(request.POST)
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save()
            formset.instance = product
            formset.save()

            return redirect('products')
    else:
        product_form = ProductForm()
        formset = SupplierProductPriceSet()

    context = {'form': product_form,
               'formset': formset}

    return render(request, 'procurement/productNew.html', context=context)

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'procurement/productDetails.html', context=context)

def update_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = SupplierProductPriceSet(request.POST)

        if product_form.is_valid() and formset.is_valid():
            print("here product form of update")
            product_form.save()
            for form in formset:
                form.instance.product = product
            formset.save()
        else:
            for form in formset:
                print(form.errors)
        #formset.save()

        print("redirect update product")

        return redirect('product_details', product_id=product_id)

    else:
        product_form = ProductForm(instance=product)

        formset = SupplierProductPriceSet(queryset=product.supplier_product.all())
        print("herer supplier product", flush=True)
        print(product.supplier_product.all(), flush=True)
        context = {'product_form': product_form,
                   'formset': formset}
        return render(request, 'procurement/productUpdate.html', context=context)



def purchase_orders(request):
    return render(request, 'procurement/purchase_orders.html')

def purchases(request):
    return render(request, 'procurement/purchases.html')