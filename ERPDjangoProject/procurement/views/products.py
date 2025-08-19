import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from ..filters import ProductFilter
from ..forms import ProductForm, SupplierProductPriceSet
from ..models import Product, Supplier
from urllib.parse import urlencode
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required()
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


@login_required
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

class ProductDetails:
    def __init__(self):
        self.request = None
        self.product_id = None
        self.product_object = None
        self.tab_name = None
        self.product_form = None
        self.formset = None

    @login_required
    def __call__(self, request, product_id):
        self.product_id = product_id
        self.request = request
        self.product_object = Product.objects.get(id=product_id)

        self.product_form = ProductForm(instance=self.product_object)
        self.formset = SupplierProductPriceSet(prefix="supplier", instance=self.product_object)


        if self.request.method == 'POST':
            self.tab_name = self.request.POST.get('tab-name')
            form_id = self.request.POST.get('form_id')
            if form_id == "product-details":
                return self.post_product_details()
            if form_id == "update-supplier-products":
                return self.post_supplier_products()
        else:
            self.tab_name = self.request.GET.get('tab-name')
            return self.render()


    def post_product_details(self):
        self.product_form = ProductForm(self.request.POST, instance=self.product_object)
        logging.info(self.product_form.is_valid())
        if self.product_form.is_valid():
            self.product_form.save()
            return self.redirect()

        else:
            logging.info("errors product details")
            logging.info(self.product_form.errors)
            return self.render()

    def post_supplier_products(self):
        self.formset = SupplierProductPriceSet(self.request.POST, prefix="supplier", instance=self.product_object)
        logging.info(self.formset.is_valid())

        if self.formset.is_valid():
            self.formset.save()
            return self.redirect()

        else:
            logging.info("errors supplier product formset")
            logging.info(self.formset.errors)
            return self.render()

    def render(self):
        context = {'product_form': self.product_form,
                   'formset': self.formset,
                   'tab_name': self.tab_name,}
        return render(self.request, 'procurement/products/details.html', context=context)

    def redirect(self):
        url = reverse('product_details', kwargs={'product_id': self.product_id})
        params = {'tab-name': self.tab_name }
        url = f"{url}?{urlencode(params)}"
        return redirect(url)



@login_required
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
