import logging

from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages

from ..filters import SupplierProductFilter
from ..forms import SupplierForm, SupplierContactSet, SupplierBankSet, ProductSupplierFormSet, SupplierAddProductForm
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
    return render(request, 'procurement/supplier/suppliers.html', context=context)


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
        print("request post",request.POST, flush=True)
        supplier_form = SupplierForm(instance=supplier)
        if form_id == "supplier-basic-information":
            supplier_form = SupplierForm(request.POST, instance=supplier)
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
                log.info("invalid supplier form")
                log.info(supplier_form.errors)

        product_form_set = ProductSupplierFormSet(instance=supplier)
        if form_id == "update-products":
            product_form_set = ProductSupplierFormSet(request.POST, instance=supplier)
            if product_form_set.is_valid():
                logging.info("valid product form set")
                product_form_set.save()
                url = reverse('supplier_details', kwargs={'supplier_id': supplier_id})
                params = {'form_id': form_id}
                params.update(filter_data)
                url = f"{url}?{urlencode(params)}"

                return redirect(url)
            else:
                logging.info("invalid product form set")
                logging.info(product_form_set.errors)
                logging.info(product_form_set.non_form_errors())

        new_product_form = SupplierAddProductForm(supplier=supplier)
        if form_id == "create-new-product":
            new_product_form = SupplierAddProductForm(request.POST, supplier=supplier)
            if new_product_form.is_valid():
                logging.info("valid product form set")
                new_product_form.save()
                url = reverse('supplier_details', kwargs={'supplier_id': supplier_id})
                params = {'form_id': form_id}
                params.update(filter_data)
                url = f"{url}?{urlencode(params)}"

                return redirect(url)
            else:
                logging.info("invalid product form set")
                logging.info(new_product_form.errors)

        contacts_form_set = SupplierContactSet(instance=supplier)
        if form_id == "update-supplier-contacts":
            contacts_form_set = SupplierContactSet(request.POST, instance=supplier)
            if contacts_form_set.is_valid():
                logging.info("valid contacts form set")
                contacts_form_set.save()
                url = reverse('supplier_details', kwargs={'supplier_id': supplier_id})
                params = {'form_id': form_id}
                params.update(filter_data)
                url = f"{url}?{urlencode(params)}"
                return redirect(url)
            else:
                logging.error("invalid contacts form set")
                logging.error(request.POST)
                logging.error(contacts_form_set.errors)


    else:
        supplier_form = SupplierForm(instance=supplier)
        product_form_set = ProductSupplierFormSet(instance=supplier)
        form_id = request.GET.get('form_id')
        contacts_form_set = SupplierContactSet(instance=supplier)
        new_product_form = SupplierAddProductForm(supplier=supplier)


    log.info(f"form id {form_id}")
    log.info(f"form supplier {supplier_form.errors}")
    log.info(f"go to get path")
    paginator = Paginator(products_filter.qs, 10)
    page = request.GET.get('page')
    if page:
        form_id = 'update-products'
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)

    logging.info("total objects")
    logging.info(objects)
    logging.info(len(objects))

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
        'contacts_form_set': contacts_form_set,
        'product_pages': objects,
        'new_product_form': new_product_form,
        'form_id': form_id,
    }

    return render(request, 'procurement/supplier/details.html', context=context)


def create_supplier(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)

        if supplier_form.is_valid():
            supplier_object = supplier_form.save()
            return redirect('supplier_details', supplier_id=supplier_object.id)

        logging.info(supplier_form.errors)

    else:
        supplier_form = SupplierForm()
        for field in supplier_form.fields.values():
            field.widget.attrs['readonly'] = False


    context = {'form': supplier_form}

    return render(request, 'procurement/supplier/new.html', context=context)
