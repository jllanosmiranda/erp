import logging

from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import redirect, render

from ..filters import SupplierProductFilter
from ..forms import SupplierForm, SupplierContactSet, SupplierBankSet
from ..models import Supplier


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
    if request.method == 'GET':
        supplier = Supplier.objects.get(id=supplier_id)
        products = supplier.products.all()
        products_filter = SupplierProductFilter(request.GET, queryset=products)
        paginator = Paginator(products_filter.qs, 10)
        page = request.GET.get('page')
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        context = {
            "supplier": supplier,
            "filter": products_filter,
            "products": objects
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
        return render(request, 'procurement/suppliers/supplierUpdate.html', context=context)
