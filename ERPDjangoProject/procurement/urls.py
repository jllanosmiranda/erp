
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name="products"),
    path('products/new', views.new_product, name='product_new'),
    path('products/<int:product_id>', views.product_details, name='product_details'),
    path('products/update/<int:product_id>', views.update_product, name='product_update'),
    path('suppliers/', views.suppliers, name='suppliers'),
    ]
