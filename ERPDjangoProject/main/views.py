from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import Business, PurchaseSettings
from main.forms import BusinessForm, PurchaseSettingsForm
import logging

log = logging.getLogger(__name__)

# Create your views here.
@login_required
def redirect_to_home(request):
    return redirect('/home')

@login_required
def home(request):
    return render(request,'main/index.html')


@login_required
def business(request):
    business_object = Business.get_solo()
    if request.method == 'POST':
        business_form = BusinessForm(request.POST, instance=business_object)
        if business_form.is_valid():
            business_form.save()
            return redirect('settings_business')

    business_form = BusinessForm(instance=business_object)
    context = {'form': business_form}
    return render(request, 'main/business.html', context=context)

@login_required
def purchase(request):
    if request.method == 'POST':
        log.info(f"request user f{request.user}")
        purchase_settings_form =  PurchaseSettingsForm(request.POST, user=request.user)
        if purchase_settings_form.is_valid():
            purchase_settings_form.save()
            return redirect('settings_purchase')

    purchase_settings_form = PurchaseSettingsForm()
    if PurchaseSettings.objects.exists():
        purchase_settings = PurchaseSettings.objects.latest('created_at')
        purchase_settings_form = PurchaseSettingsForm(instance=purchase_settings)

    context = {'form': purchase_settings_form}
    return render(request, 'main/purchase.html', context=context)

