
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name="products"),
    path('products/new', views.new_product, name='product_new'),
    path('products/<int:product_id>', views.product_details, name='product_details'),
    path('products/update/<int:product_id>', views.update_product, name='product_update'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/<int:supplier_id>', views.view_supplier_details, name='supplier_details'),

    path('suppliers/new', views.create_supplier, name='create_supplier'),

    path('goods', views.good_receipt_note_list, name='good_receipt_note_list'),
    path('goods/new', views.good_receipt_note_new, name='good_receipt_note_new'),
    path('goods/item/<int:supplier_id>/<int:extra>', views.good_receipt_note_supplier_products, name='good_receipt_note_products'),
    path('purchase-requisitions/', views.purchase_requisition_list, name='purchase_requisition_list'),

    ]
