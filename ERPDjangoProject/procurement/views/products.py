import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from ..filters import ProductFilter
from ..forms import ProductForm, SupplierProductSet, SupplierProductUpdateForm, AssignSupplierToProductForm
from procurement.models import Product, Supplier, SupplierProduct
from urllib.parse import urlencode
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import logging
from procurement.filters import SupplierFilter

log = logging.getLogger(__name__)


@login_required()
def list(request):

    products_list = Product.objects.all()
    product_filter = ProductFilter(request.GET,
                                    queryset=products_list)
    log.info(f"product filter {product_filter}")

    paginator = Paginator(product_filter.qs, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    log.info(f"filter {product_filter.form.cleaned_data}")
    filters_for_url = {
        k: v for k,v in product_filter.form.cleaned_data.items() if v not in [None, '']
    }
    extra_filters =urlencode(filters_for_url)

    context = {'page_obj': page_object,
               'filter': product_filter,
               'extra_filters': extra_filters,
               'title': 'Productos'}

    return render(request, 'procurement/products/pages/list.html', context=context)


@login_required
def new_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        log.info(f"request {request.POST}")
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user
            product.updated_by = request.user
            product.save()
            return redirect('product_details', product_id=product.id)
        else:
            logging.info(product_form.errors)
            context = {'form': product_form}
            logging.info(f"context {context}")
            return render(request, 'procurement/products/pages/new.html', context=context)
    product_form = ProductForm()

    context = {'form': product_form}

    return render(request, 'procurement/products/pages/new.html', context=context)


@login_required
def details(request, product_id):
    product_object = Product.objects.get(id=product_id)

    tab_name = request.GET.get('tab-name')
    form_id = request.GET.get('form_id')
    if form_id == "suppliers":
        tab_name = "suppliers"

    log.info(f"tab name: {tab_name}")
    log.info(f"form id {form_id}")

    context = {'product': product_object,
               'tab_name': tab_name}
    return render(request, 'procurement/products/pages/details.html', context=context)

def suppliers_of_product(request, product_id):
    product_object = Product.objects.get(id=product_id)
    supplier_filter = SupplierFilter(request.GET, queryset=product_object.suppliers.all())
    paginator = Paginator(supplier_filter.qs, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'product': product_object,
               'supplier_products': page_object,
    }

    return render(request, 'procurement/products/pages/supplierOfProduct.html', context=context)

@login_required
def edit_basic_information(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.updated_by = request.user
            product.save()
            return redirect('product_details', product_id=product.id)
        else:
            logging.info(product_form.errors)
            context = {'form': product_form}
            return render(request, template_name='procurement/products/pages/editBasicInformation.html', context=context)

    product_form = ProductForm(instance=product)
    context = {'form': product_form}
    return render(request, template_name='procurement/products/pages/editBasicInformation.html', context=context)

@login_required
def add_new_supplier(request, product_id):
    product = Product.objects.get(id=product_id)
    supplier_product = SupplierProduct(product=product)
    if request.method == 'POST':
        assign_supplier_to_product_form = AssignSupplierToProductForm(request.POST, instance=supplier_product)
        if assign_supplier_to_product_form.is_valid():
            log.info("valid supplier product set form")
            supplier_product = assign_supplier_to_product_form.save(commit=False)
            supplier_product.product = product
            supplier_product.created_by = request.user
            supplier_product.updated_by = request.user
            supplier_product.save()
            return redirect('product_details', product_id=product.id)
        else:
            log.info(assign_supplier_to_product_form.errors)
            context = {'form': assign_supplier_to_product_form,
                       'product': product}
            return render(request, template_name='procurement/products/pages/assignSupplierToProduct.html', context=context)

    assign_supplier_to_product_form = AssignSupplierToProductForm(instance=supplier_product)
    context = {'form': assign_supplier_to_product_form,
               'product': product,}
    return render(request, template_name='procurement/products/pages/assignSupplierToProduct.html', context=context)

@login_required
def edit_supplier_of_products(request, supplier_product_id):
    supplier_product_object = SupplierProduct.objects.get(id=supplier_product_id)
    if request.method == 'POST':
        supplier_product_form = SupplierProductUpdateForm(request.POST, instance=supplier_product_object)
        if supplier_product_form.is_valid():
            log.info("valid supplier product set form")
            supplier_product = supplier_product_form.save(commit=False)
            supplier_product.updated_by = request.user
            supplier_product.save()
            return redirect('product_details', product_id=supplier_product_object.product.id)
        else:
            log.info(supplier_product_form.errors)
            context = {'form': supplier_product_form,
                       'product': supplier_product_object.product,}
            return render(request, template_name='procurement/products/pages/editSupplierOfProduct.html', context=context)

    supplier_product_form = SupplierProductUpdateForm(instance=supplier_product_object)
    context = {'form': supplier_product_form,
               'product': supplier_product_object.product,}
    return render(request, template_name='procurement/products/pages/editSupplierOfProduct.html', context=context)


@login_required
def new_product_from_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        suppliers_formset = SupplierProductSet(request.POST, prefix="supplier")

        logging.info(f"supplier {suppliers_formset}")

        if product_form.is_valid() and suppliers_formset.is_valid():
            product = product_form.save()
            for supplier_form in suppliers_formset:
                supplier_form.instance.product = product
                supplier_form.save()

            return redirect('product_details', product_id=product.id)
        else:
            logging.info(product_form.errors)
            logging.info(suppliers_formset.errors)
            context = {'form': product_form,
                       'suppliers_formset': suppliers_formset}
            logging.info(f"context {context}")
            return render(request, 'procurement/products/pages/new.html', context=context)
    else:
        product_form = ProductForm()
        initial_data = [{'supplier': supplier}]
        suppliers_formset = SupplierProductSet(prefix="supplier",
                                                    initial=initial_data)

    context = {'form': product_form,
               'suppliers_formset': suppliers_formset}

    return render(request, 'procurement/products/pages/new.html', context=context)
