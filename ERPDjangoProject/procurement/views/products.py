import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from ..filters import ProductFilter
from ..forms import ProductForm, SupplierProductPriceSet
from ..models import Product, Supplier
from urllib.parse import urlencode
from django.urls import reverse


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

    return render(request, 'procurement/products/list.html', context=context)


def new_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        suppliers_formset = SupplierProductPriceSet(request.POST, prefix="supplier")
        if product_form.is_valid() and suppliers_formset.is_valid():
            product = product_form.save()
            for form in suppliers_formset:
                form.instance.product = product
                form.save()
            return redirect('product_details', product_id=product.id)
        else:
            logging.info(product_form.errors)
            logging.info(suppliers_formset.errors)
            context = {'form': product_form,
                       'suppliers_formset': suppliers_formset}
            logging.info(f"context {context}")
            return render(request, 'procurement/products/new.html', context=context)
    else:
        product_form = ProductForm()
        suppliers_formset = SupplierProductPriceSet(prefix="supplier")

    context = {'form': product_form,
               'suppliers_formset': suppliers_formset}

    return render(request, 'procurement/products/new.html', context=context)


def product_details(request, product_id):
    print("update product id", product_id, flush=True)
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        logging.info('info')
        logging.info(request.POST)

        logging.info("here update post")

        if form_id == "product-details":
            product_form = ProductForm(request.POST, instance=product)
            formset = SupplierProductPriceSet(prefix="supplier", instance=product)
            logging.info(product_form.is_valid())
            if product_form.is_valid():
                product_form.save()
                url = reverse('product_details', kwargs={'product_id': product_id})
                params = {'tab-name': 'product-details',}
                url = f"{url}?{urlencode(params)}"
                return redirect(url)

            else:
                logging.info("errors product details")
                logging.info(product_form.errors)
                context = {'product_form': product_form,
                           'formset': formset,
                           'tab_name': 'product-details',}
                return render(request, 'procurement/products/details.html', context=context)

        if form_id == "update-supplier-products":
            product_form = ProductForm(instance=product)
            formset = SupplierProductPriceSet(request.POST, prefix="supplier", instance=product)
            logging.info(formset.is_valid())

            if formset.is_valid():
                formset.save()
                url = reverse('product_details', kwargs={'product_id': product_id})
                params = {'tab-name': 'update-supplier-products'}
                url = f"{url}?{urlencode(params)}"
                return redirect(url)
            else:
                logging.info("errors supplier product formset")
                logging.info(formset.errors)
                context = {'product_form': product_form,
                           'formset': formset,
                           'tab_name': 'update-supplier-products'}
                return render(request, 'procurement/products/details.html', context=context)


    else:
        product_form = ProductForm(instance=product)
        formset = SupplierProductPriceSet(prefix="supplier", instance=product)
        tab_name = request.GET.get('tab-name')

        #formset = SupplierProductPriceSet(queryset=product.supplier_product.all())
        print("herer supplier products", flush=True)
        print(product.supplier_product.all(), flush=True)
        context = {'product_form': product_form,
                   'formset': formset,
                   'tab_name': tab_name,}
        return render(request, 'procurement/products/details.html', context=context)


def new_product_from_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        suppliers_formset = SupplierProductPriceSet(request.POST, prefix="supplier")

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
            return render(request, 'procurement/products/new.html', context=context)
    else:
        product_form = ProductForm()
        initial_data = [{'supplier': supplier}]
        suppliers_formset = SupplierProductPriceSet(prefix="supplier",
                                                    initial=initial_data)

    context = {'form': product_form,
               'suppliers_formset': suppliers_formset}

    return render(request, 'procurement/products/new.html', context=context)
