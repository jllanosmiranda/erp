import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from ..filters import ProductFilter
from ..forms import ProductForm, SupplierProductPriceSet
from ..models import Product, Supplier, SupplierProduct
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
        suppliers_formset = SupplierProductPriceSet(request.POST, prefix="supplier")
        log.info(f"request {request.POST}")
        log.info(f"suppliers {suppliers_formset}")
        if product_form.is_valid() and suppliers_formset.is_valid():
            product = product_form.save(commit=False)
            product._changed_by = request.user
            product.save()
            for form in suppliers_formset:
                if form.has_changed():
                    form.instance.product = product
                    supplier_product_object = form.save(commit=False)
                    supplier_product_object._changed_by = request.user
                    supplier_product_object.save()
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
        suppliers_formset = SupplierProductPriceSet(prefix="supplier")

    context = {'form': product_form,
               'suppliers_formset': suppliers_formset}

    return render(request, 'procurement/products/pages/new.html', context=context)


class ProductDetails:
    def __init__(self):
        self.request = None
        self.product_id = None
        self.product_object = None
        self.tab_name = None
        self.product_form = None
        self.formset = None

    def __call__(self, request, product_id):
        self.product_id = product_id
        self.request = request
        self.product_object = Product.objects.get(id=product_id)

        self.product_form = ProductForm(instance=self.product_object)
        self.formset = SupplierProductPriceSet(prefix="supplier", instance=self.product_object)
        self.supplier_filter = SupplierFilter(request.GET, queryset=self.product_object.suppliers.all())

        self.form_id = None

        if self.request.method == 'POST':
            self.tab_name = self.request.POST.get('tab-name')
            self.form_id = self.request.POST.get('form_id')
            form_id = self.request.POST.get('form_id')
            if form_id == "product-details":
                return self.post_product_details()
            if form_id == "update-supplier-products":
                return self.post_supplier_products()
        else:
            self.tab_name = self.request.GET.get('tab-name')
            self.form_id = self.request.GET.get('form_id')
            if self.form_id == "suppliers":
                self.tab_name = "suppliers"
            return self._get()


    def post_product_details(self):
        self.product_form = ProductForm(self.request.POST, instance=self.product_object)
        logging.info(self.product_form.is_valid())
        if self.product_form.is_valid():
            product = self.product_form.save(commit=False)
            product._changed_by = self.request.user
            product.save()
            return self.redirect()

        else:
            logging.info("errors product details")
            logging.info(self.product_form.errors)
            return self.render()

    def post_supplier_products(self):
        self.formset = SupplierProductPriceSet(self.request.POST, prefix="supplier", instance=self.product_object)
        logging.info(self.formset.is_valid())

        if self.formset.is_valid():
            formset = self.formset.save(commit=False)
            for obj in formset:
                obj._changed_by = self.request.user
                obj.save()
            logging.info(
                f"formset {self.formset.save(commit=False)}"
            )
            return self.redirect()

        else:
            logging.info("errors supplier product formset")
            logging.info(self.formset.errors)
            return self.render()

    def render(self):
        logging.info(f"tab name: {self.tab_name}")
        context = {'product_form': self.product_form,
                   'formset': self.formset,
                   'tab_name': self.tab_name,
                   'filter': self.supplier_filter,}
        return render(self.request, 'procurement/products/pages/details.html', context=context)

    def _get(self):
        paginator = Paginator(self.supplier_filter.qs, 10)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)
        suppliers_products = SupplierProduct.objects.filter(product=self.product_object,
                                                   supplier__in=page_object)
        log.info(f"supplier products {suppliers_products}")

        self.formset = SupplierProductPriceSet(prefix="supplier",
                                               instance=self.product_object,
                                               queryset=suppliers_products)
        return self.render()

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
            return render(request, 'procurement/products/pages/new.html', context=context)
    else:
        product_form = ProductForm()
        initial_data = [{'supplier': supplier}]
        suppliers_formset = SupplierProductPriceSet(prefix="supplier",
                                                    initial=initial_data)

    context = {'form': product_form,
               'suppliers_formset': suppliers_formset}

    return render(request, 'procurement/products/pages/new.html', context=context)
