
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
    path('suppliers/update<int:supplier_id>', views.update_supplier, name='update_supplier'),

    path('goods', views.good_receipt_order, name='good_receipt_note_new'),
    path('goods-products/<int:supplier_id>/<int:extra>', views.good_receipt_note_supplier_products, name='good_receipt_note_products'),
    ]
