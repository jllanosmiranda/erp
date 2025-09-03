from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='root'),
    path('home/', views.home, name='home'),
    path('settings/business/', views.business, name='settings_business'),
    path('settings/purchase/', views.purchase, name='settings_purchase')
]
