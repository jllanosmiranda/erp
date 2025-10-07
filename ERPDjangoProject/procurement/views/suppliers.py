import logging

from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from ..filters import SupplierProductFilter
from ..forms import SupplierForm, SupplierContactSet, SupplierBankSet, ProductSupplierFormSet, SupplierAddProductForm
from ..models import Supplier, SupplierProduct
from procurement.filters import SupplierFilter

log = logging.getLogger(__name__)


@login_required
def list(request):
    supplier_list = Supplier.objects.all()
    supplier_filter = SupplierFilter(request.GET,
                                   queryset=supplier_list)

    paginator = Paginator(supplier_filter.qs, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    filters_for_url = {
        k: v for k,v in supplier_filter.form.cleaned_data.items() if v not in [None, '']
    }
    extra_filters =urlencode(filters_for_url)

    context = {'page_obj': page_object,
               'filter': supplier_filter,
               'extra_filters': extra_filters}
    return render(request, 'procurement/supplier/pages/list.html', context=context)


@login_required
def view_basic_information(request, supplier_id):
        supplier_id = supplier_id
        request = request
        supplier_object = Supplier.objects.get(id=supplier_id)
        tab_name = "basic-information"

        context = {
            "supplier": supplier_object,
            'tab_name': tab_name,
        }

        return render(request, 'procurement/supplier/pages/basicInformation.html', context=context)

@login_required
def view_products(request, supplier_id):
    supplier_id = supplier_id
    supplier_object = Supplier.objects.get(id=supplier_id)

    products_objects = supplier_object.products.all()
    products_filter = SupplierProductFilter(request.GET, queryset=products_objects)
    supplier_products = SupplierProduct.objects.filter(supplier=supplier_object,
                                                       product__in=products_filter.qs)
    logging.info(f"products filter {products_filter.data}")

    paginator = Paginator(supplier_products, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    tabname = "product-list"

    context = {
        "supplier": supplier_object,
        "supplier_products": page_object,
        'tab_name': tabname,
    }

    return render(request, 'procurement/supplier/pages/productList.html', context=context)

@login_required
def view_contacts(request, supplier_id):
    supplier_object = Supplier.objects.get(id=supplier_id)
    tabname = "contact-list"

    context = {
        "supplier": supplier_object,
        "contacts": [],
        'tab_name': tabname,
    }

    return render(request, 'procurement/supplier/pages/contactList.html', context=context)

@login_required
def edit_supplier_basic_information(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST, instance=supplier)
        if supplier_form.is_valid():
            log.info("valid supplier form")
            supplier_object = supplier_form.save(commit=False)
            supplier_object.updated_by = request.user
            supplier_object.save()
            return redirect('supplier_basic_information', supplier_id=supplier_id)
        else:
            log.info("invalid supplier form")
            log.info(supplier_form.errors)
            context = {'form': supplier_form,
                       'supplier': supplier}
            return render(request, template_name='procurement/supplier/pages/editBasicInformation.html', context=context)

    supplier_form = SupplierForm(instance=supplier)
    context = {'form': supplier_form,
               'supplier': supplier}

    return render(request, template_name='procurement/supplier/pages/editBasicInformation.html', context=context)



@login_required
def create_supplier(request):
    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)

        if supplier_form.is_valid():
            supplier_object = supplier_form.save(commit=False)
            supplier_object.created_by = request.user
            supplier_object.updated_by = request.user
            supplier_object.save()
            return redirect('supplier_basic_information', supplier_id=supplier_object.id)

        logging.info(supplier_form.errors)

    else:
        supplier_form = SupplierForm()
        for field in supplier_form.fields.values():
            field.widget.attrs['readonly'] = False


    context = {'form': supplier_form}

    return render(request, 'procurement/supplier/pages/new.html', context=context)

@login_required
def get_supplier_products(request, supplier_product_id):
    object = SupplierProduct.objects.get(id=supplier_product_id)
    return JsonResponse({
        'name': object.product.product_name,
        'price': object.price,
        'currency': object.currency,
        'unit_of_measure': object.unit_of_measure
    })

