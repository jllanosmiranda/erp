import logging

from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages

from ..filters import SupplierProductFilter
from ..forms import SupplierForm, SupplierContactSet, SupplierBankSet, ProductSupplierFormSet
from ..models import Supplier, SupplierProduct

log = logging.getLogger(__name__)


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


def view_supplier_details(request, supplier_id):
    print("request get",request.GET, flush=True)
    log.info(f"supplier id {supplier_id}")
    supplier = Supplier.objects.get(id=supplier_id)
    products = supplier.products.all()
    products_filter = SupplierProductFilter(request.GET, queryset=products)
    logging.info(f"products filter {products_filter.data}")

    filter_data = {}
    if products_filter.data:
        filter_data = products_filter.data.dict()


    form_id = None
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        supplier_form = SupplierForm(request.POST, instance=supplier)
        print("request post",request.POST, flush=True)
        if form_id == "supplier-basic-information":
            if supplier_form.is_valid():
                supplier_form.save()
                url = reverse('supplier_details', kwargs={'supplier_id': supplier_id})
                params = {'form_id': form_id}
                params.update(filter_data)
                url = f"{url}?{urlencode(params)}"
                messages.success(request, 'Supplier updated successfully')
                return redirect(url)
            else:
                messages.error(request, 'Supplier updated error')
                log.info("invalid supplier")
                log.info(supplier_form.errors)

        product_form_set = ProductSupplierFormSet(request.POST,instance=supplier)
        if form_id == "supplier_products":
            if product_form_set.is_valid():
                logging.info("valid form set")
                product_form_set.save()
                url = reverse('supplier_details', kwargs={'supplier_id': supplier_id})
                params = {'form_id': form_id}
                params.update(filter_data)
                url = f"{url}?{urlencode(params)}"

                return redirect(url)
            else:
                logging.info("invalid form set")
                logging.info(product_form_set.errors)
                logging.info(product_form_set.non_form_errors())


    else:
        supplier_form = SupplierForm(instance=supplier)
        product_form_set = ProductSupplierFormSet(instance=supplier)
        form_id = request.GET.get('form_id')


    log.info(f"form id {form_id}")
    log.info(f"form supplier {supplier_form.errors}")
    log.info(f"go to get path")
    paginator = Paginator(products_filter.qs, 10)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)

    logging.info("total objects")
    logging.info(objects)
    logging.info(len(objects))

    for o in objects:
        logging.info("datos")
        logging.info(o)

    suppliers_objects = SupplierProduct.objects.filter(
        supplier=supplier,
        product__in=objects)

    product_form_set = ProductSupplierFormSet(instance=supplier,
                                              queryset=suppliers_objects)
    context = {
        "supplier": supplier,
        "supplier_form": supplier_form,
        "filter": products_filter,
        "products": suppliers_objects,
        'products_forms': product_form_set,
        'form_id': form_id,
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
        product_form_set = ProductSupplierFormSet(request.POST, instance=supplier)

        if supplier_form.is_valid() and supplier_contact_form_set.is_valid() and supplier_bank_form_set.is_valid() and product_form_set.is_valid():
            logging.info("valid update supplier")
            supplier_object = supplier_form.save()
            supplier_contact_form_set.save()
            supplier_bank_form_set.save()
            f = product_form_set.save()
            logging.info(f)


            return redirect('supplier_details', supplier_id=supplier_object.id)
        else:
            logging.info("invalid update supplier")
            logging.info(supplier_form.errors)
            logging.info(supplier_contact_form_set.errors)
            logging.info(supplier_bank_form_set.errors)
            logging.info(product_form_set.errors)
            context = {'form': supplier_form,
                       'supplier_contact_form_set': supplier_contact_form_set,
                       'supplier_bank_form_set': supplier_bank_form_set,
                       'product_form_set': product_form_set,}
            return render(request, 'procurement/suppliers/supplierUpdate.html', context=context)
    else:
        supplier_form = SupplierForm(instance=supplier)
        supplier_contact_form_set = SupplierContactSet(instance=supplier)
        supplier_bank_form_set = SupplierBankSet(instance=supplier)
        product_form_set = ProductSupplierFormSet(instance=supplier)
        context = {'form': supplier_form,
                   'supplier_contact_form_set': supplier_contact_form_set,
                   'supplier_bank_form_set': supplier_bank_form_set,
                   'product_form_set': product_form_set}
        return render(request, 'procurement/suppliers/supplierUpdate.html', context=context)
