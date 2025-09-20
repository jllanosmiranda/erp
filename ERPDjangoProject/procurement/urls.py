
from django.urls import path

from .views import products, suppliers, good_receipt_notes, purchase_requirements

urlpatterns = [
    path('products/', products.list, name="products"),
    path('products/new', products.new_product, name='product_new'),
    path('products/<int:product_id>', products.details, name='product_details'),
    path('products/<int:product_id>/basic_information', products.edit_basic_information, name='product_edit_basic_information'),
    path('products/<int:product_id>/supplier', products.add_new_supplier, name='add_supplier_to_product'),
    path('supplier_products/<int:supplier_product_id>/', products.edit_supplier_of_products, name='edit_supplier_of_product'),
    path('suppliers/', suppliers.list, name='suppliers'),
    path('suppliers/<int:supplier_id>/basic-information', suppliers.view_basic_information, name='supplier_basic_information'),
    path('suppliers/<int:supplier_id>/contacts', suppliers.view_contacts, name='supplier_contacts'),
    path('suppliers/<int:supplier_id>/products', suppliers.view_products, name='supplier_products'),
    path('suppliers/<int:supplier_id>/edit', suppliers.edit_supplier_basic_information, name='supplier_edit_basic_information'),

    path('suppliers/new', suppliers.create_supplier, name='create_supplier'),
    path('suppliers/<int:supplier_id>/product', products.new_product_from_supplier, name='new_product_from_supplier'),

    path('goods', good_receipt_notes.good_receipt_order, name='good_receipt_note_new'),
    path('goods-products/<int:supplier_id>/<int:extra>',
         good_receipt_notes.good_receipt_note_supplier_products, name='good_receipt_note_products'),
         
    # Purchase Requirements
    path('purchase-requirements/', purchase_requirements.purchase_requirement_list, name='purchase_requirement_list'),
    path('purchase-requirements/create/', purchase_requirements.purchase_requirement_create, name='purchase_requirement_create'),
    path('purchase-requirements/<int:pk>/', purchase_requirements.purchase_requirement_detail, name='purchase_requirement_detail'),
    path('purchase-requirements/supplier-products/<int:supplier_id>/', purchase_requirements.get_supplier_products, name='purchase_requirement_supplier_products'),

    path('supplier-product/<int:supplier_product_id>/', suppliers.get_supplier_products, name='new_product_from_supplier'),
    ]
