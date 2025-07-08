
from django.urls import path

from .views import products, suppliers, good_receipt_notes

urlpatterns = [
    path('products/', products.products, name="products"),
    path('products/new', products.new_product, name='product_new'),
    path('products/<int:product_id>', products.product_details, name='product_details'),
    path('products/update/<int:product_id>', products.update_product, name='product_update'),
    path('suppliers/', suppliers.suppliers, name='suppliers'),
    path('suppliers/<int:supplier_id>', suppliers.view_supplier_details, name='supplier_details'),

    path('suppliers/new', suppliers.create_supplier, name='create_supplier'),
    path('suppliers/update/<int:supplier_id>', suppliers.update_supplier, name='update_supplier'),
    path('suppliers/<int:supplier_id>/product', products.new_product_from_supplier, name='new_product_from_supplier'),

    path('goods', good_receipt_notes.good_receipt_order, name='good_receipt_note_new'),
    path('goods-products/<int:supplier_id>/<int:extra>',
         good_receipt_notes.good_receipt_note_supplier_products, name='good_receipt_note_products'),
    ]
