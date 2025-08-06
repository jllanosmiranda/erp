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


def list(request):

    suppliers = Supplier.objects.all()
    context = {'suppliers': suppliers}
    return render(request, 'procurement/supplier/list.html', context=context)


class SupplierDetails:
    def __init__(self):
        self.request = None
        self.supplier_id = None
        self.supplier_object = None
        self.tab_name = None
        self.supplier_form = None
        self.formset = None
        self.product_form = None
        self.product_formset = None
        self.products_filter = None
        self.suppliers_objects = None
        self.objects = None
        self.filter_data = dict()

    def __call__(self, request, supplier_id):
        self.supplier_id = supplier_id
        self.request = request
        self.supplier_object = Supplier.objects.get(id=supplier_id)

        print("request get", request.GET, flush=True)
        log.info(f"supplier id {supplier_id}")
        products = self.supplier_object.products.all()
        self.products_filter = SupplierProductFilter(request.GET, queryset=products)
        logging.info(f"products filter {self.products_filter.data}")

        if self.products_filter.data:
            self.filter_data = self.products_filter.data.dict()

        self.supplier_form = SupplierForm(instance=self.supplier_object)
        self.product_form_set = ProductSupplierFormSet(instance=self.supplier_object)
        self.new_product_form = SupplierAddProductForm(supplier=self.supplier_object)
        self.contacts_form_set = SupplierContactSet(instance=self.supplier_object)

        if self.request.method == 'POST':
            self.tab_name = self.request.POST.get('tab-name')
            self.form_id = self.request.POST.get('form_id')
            print("request post",request.POST, flush=True)
            if self.form_id == "supplier-basic-information":
                return self._basic_information()

            if self.form_id == "update-products":
                return self._product_list()

            if self.form_id == "create-new-product":
                return self._create_new_product()

            if self.form_id == "update-supplier-contacts":
                return self._contacts()


        else:
            self.form_id = request.GET.get('form_id')
            self.tab_name = request.GET.get('tab-name')
            return self._get()

    def _redirect(self):
        url = reverse('supplier_details', kwargs={'supplier_id': self.supplier_id})
        params = {'form_id': self.form_id,
                  'tab-name': self.tab_name, }
        self.filter_data.update(params)
        url = f"{url}?{urlencode(self.filter_data)}"
        log.info(url)

        return redirect(url)

    def _render(self):
        context = {
            "supplier": self.supplier_object,
            "supplier_form": self.supplier_form,
            "filter": self.products_filter,
            "products": self.suppliers_objects,
            'products_forms': self.product_form_set,
            'contacts_form_set': self.contacts_form_set,
            'product_pages': self.objects,
            'new_product_form': self.new_product_form,
            'form_id': self.form_id,
            'tab_name': self.tab_name,
        }

        return render(self.request, 'procurement/supplier/details.html', context=context)

    def _product_list(self):
        product_form_set = ProductSupplierFormSet(self.request.POST, instance=self.supplier_object)
        if product_form_set.is_valid():
            logging.info("valid product form set")
            product_form_set.save()
            return self._redirect()
        else:
            logging.info("invalid product form set")
            logging.info(product_form_set.errors)
            logging.info(product_form_set.non_form_errors())
            return self._render()

    def _basic_information(self):
        supplier_form = SupplierForm(self.request.POST, instance=supplier)
        if supplier_form.is_valid():
            supplier_form.save()
            return self._redirect()
        else:
            messages.error(self.request, 'Supplier updated error')
            log.info("invalid supplier form")
            log.info(supplier_form.errors)
            return self._render()

    def _bank_account(self):
        pass

    def _create_new_product(self):
        new_product_form = SupplierAddProductForm(self.request.POST, supplier=self.supplier_object)
        if new_product_form.is_valid():
            logging.info("valid product form set")
            new_product_form.save()
            return self._redirect()
        else:
            logging.info("invalid product form set")
            logging.info(new_product_form.errors)
            return self._render()

    def _contacts(self):
        contacts_form_set = SupplierContactSet(self.request.POST, instance=self.supplier_object)
        if contacts_form_set.is_valid():
            logging.info("valid contacts form set")
            contacts_form_set.save()
            return self._redirect()
        else:
            logging.error("invalid contacts form set")
            logging.error(self.request.POST)
            logging.error(contacts_form_set.errors)
            return self._render()

    def _get(self):
        log.info(f"tab name: {self.tab_name}")

        log.info(f"form id {self.form_id}")
        log.info(f"form supplier {self.supplier_form.errors}")
        log.info(f"go to get path")
        paginator = Paginator(self.products_filter.qs, 10)
        page = self.request.GET.get('page')
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
            supplier=self.supplier_object,
            product__in=objects)

        self.product_form_set = ProductSupplierFormSet(instance=self.supplier_object,
                                                  queryset=suppliers_objects)

        return self._render()


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
