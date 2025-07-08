import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from ..filters import ProductFilter
from ..forms import ProductForm, SupplierProductPriceSet
from ..models import Product


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
        suppliers_formset = SupplierProductPriceSet(request.POST)
        if product_form.is_valid():
            product_form.save()

            return redirect('products')
    else:
        product_form = ProductForm()
        suppliers_formset = SupplierProductPriceSet(prefix="supplier")

    context = {'form': product_form,
               'suppliers_formset': suppliers_formset}

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
        formset = SupplierProductPriceSet(request.POST, instance=product)
        logging.info('info')
        logging.info(request.POST)

        logging.info("here update post")
        logging.info(product_form.is_valid())
        logging.info(formset.is_valid())

        if product_form.is_valid() and formset.is_valid():
            product_form.save()
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
        formset = SupplierProductPriceSet(prefix="supplier", instance=product)

        #formset = SupplierProductPriceSet(queryset=product.supplier_product.all())
        print("herer supplier products", flush=True)
        print(product.supplier_product.all(), flush=True)
        context = {'product_form': product_form,
                   'formset': formset}
        return render(request, 'procurement/products/productUpdate.html', context=context)
