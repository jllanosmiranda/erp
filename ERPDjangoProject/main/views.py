from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import Business
from main.form import BusinessForm

# Create your views here.
@login_required
def redirect_to_home(request):
    return redirect('/home')

@login_required
def home(request):
    return render(request,'main/index.html')


def business(request):
    business_object = Business.get_solo()
    if request.method == 'POST':
        business_form = BusinessForm(request.POST, instance=business_object)
        if business_form.is_valid():
            business_form.save()
            return redirect('home')

    business_form = BusinessForm(instance=business_object)
    context = {'form': business_form}
    return render(request, 'main/business.html', context=context)
