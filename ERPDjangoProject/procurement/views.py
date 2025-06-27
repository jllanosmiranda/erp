from django.shortcuts import render, redirect
from .models import Product, Supplier, SupplierProductPrice, SupplierProduct
from .forms import (ProductForm,
                    SupplierForm,
                    SupplierProductPriceSet,
                    SupplierContactSet,
                    SupplierBankSet,
                    GoodReceiptNoteForm,
                    form_set, GoodReceiptNoteItemForm)
from .filters import ProductFilter
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    return render(request, 'procurement/suppliers/suppliers.html', context=context)

def products(request):

    products_list = Product.objects.all()
    product_filter = ProductFilter(request.GET,
                                    queryset=products_list)

    paginator = Paginator(product_filter.qs, 10)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)

    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {'products': objects,
               'filter': product_filter}

    return render(request, 'procurement/products/products.html', context=context)

def new_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()

            return redirect('products')
    else:
        product_form = ProductForm()

    context = {'form': product_form}

    return render(request, 'procurement/products/productNew.html', context=context)

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    logging.info(product)
    context = {'product': product}
    return render(request, 'procurement/products/productDetails.html', context=context)

def update_product(request, product_id):
    print("update product id", product_id, flush=True)
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = SupplierProductPriceSet(request.POST)
        logging.info('info')
        logging.info(request.POST)

        logging.info("here update post")
        logging.info(product_form.is_valid())
        logging.info(formset.is_valid())

        if product_form.is_valid() and formset.is_valid():
            product_form.save()
            formset.product_instance = product
            formset.save()
        else:
            logging.info("errors")
            logging.info(product_form.errors)
            for form in formset:
                logging.info(form.errors)

        print("redirect update products")

        return redirect('product_details', product_id=product_id)

    else:
        product_form = ProductForm(instance=product)

        formset = SupplierProductPriceSet(queryset=product.supplier_product.all())
        print("herer supplier products", flush=True)
        print(product.supplier_product.all(), flush=True)
        context = {'product_form': product_form,
                   'formset': formset}
        return render(request, 'procurement/products/productUpdate.html', context=context)

def view_supplier_details(request, supplier_id):
    if request.method == 'GET':
        supplier = Supplier.objects.get(id=supplier_id)
        print("contacts", supplier.contacts.all(), flush=True)
        context = {
            "supplier": supplier
        }
        return render(request, 'procurement/suppliers/supplierDetails.html', context=context)

def create_supplier(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)
        supplier_contact_form_set = SupplierContactSet(request.POST)
        supplier_bank_form_set = SupplierBankSet(request.POST)

        if supplier_form.is_valid():
            supplier_object = supplier_form.save()
            return redirect('supplier_details', supplier_id=supplier_object.id)
        else:
            logging.info(supplier_form.errors)
            logging.info(supplier_contact_form_set.errors)
            context = {'form': supplier_form,
                       'supplier_contact_form_set': supplier_contact_form_set,
                       'supplier_bank_form_set': supplier_bank_form_set}
            return render(request, 'procurement/suppliers/supplierNew.html', context=context)

    elif request.method == 'GET':

        supplier_form = SupplierForm()
        supplier_contact_form_set = SupplierContactSet()
        supplier_bank_form_set = SupplierBankSet()

        context = {'form': supplier_form,
                   'supplier_contact_form_set': supplier_contact_form_set,
                   'supplier_bank_form_set': supplier_bank_form_set}

        return render(request, 'procurement/suppliers/supplierNew.html', context=context)

def update_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST, instance=supplier)
        supplier_contact_form_set = SupplierContactSet(request.POST, instance=supplier)
        supplier_bank_form_set = SupplierBankSet(request.POST, instance=supplier)

        if supplier_form.is_valid() and supplier_contact_form_set.is_valid() and supplier_bank_form_set.is_valid():
            supplier_object = supplier_form.save()
            contact_instances = supplier_contact_form_set.save(commit=False)
            bank_instances = supplier_bank_form_set.save(commit=False)
            for instance in contact_instances:
                instance.save()
            for instance in bank_instances:
                instance.save()

            return redirect('supplier_details', supplier_id=supplier_object.id)
        else:
            logging.info(supplier_form.errors)
            logging.info(supplier_contact_form_set.errors)
            context = {'form': supplier_form,
                       'supplier_contact_form_set': supplier_contact_form_set,
                       'supplier_bank_form_set': supplier_bank_form_set}
            return render(request, 'procurement/suppliers/supplierNew.html', context=context)
    else:
        supplier_form = SupplierForm(instance=supplier)
        supplier_contact_form_set = SupplierContactSet(instance=supplier)
        supplier_bank_form_set = SupplierBankSet(instance=supplier)
        context = {'form': supplier_form,
                   'supplier_contact_form_set': supplier_contact_form_set,
                   'supplier_bank_form_set': supplier_bank_form_set}
        return render(request, 'procurement/suppliers/supplierNew.html', context=context)



def purchase_orders(request):
    return render(request, 'procurement/purchase_orders.html')

def purchases(request):
    return render(request, 'procurement/purchases.html')


def good_receipt_order(request):
    form = GoodReceiptNoteForm()
    context = {'form': form}
    return render(request, 'procurement/good_receipt_notes/goodReceiptNoteNew.html', context=context)


def good_receipt_note_list(request):
    pass

def good_receipt_note_supplier_products(request, supplier_id, extra=1):
    GoodReceiptNoteItemSet = form_set(extra=extra)
    print("request")
    print(request)
    print(request.GET)
    if request.method == 'GET':
        formset = GoodReceiptNoteItemSet(supplier_id=supplier_id, prefix='leo')
        context = {'formset': formset}
        return render(request, 'procurement/good_receipt_notes/goodReceiptNoteItem.html', context=context)
