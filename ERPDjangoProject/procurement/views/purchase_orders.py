
from django.shortcuts import render
def purchase_orders(request):
    return render(request, 'procurement/purchase_orders.html')

def purchases(request):
    return render(request, 'procurement/purchases.html')
