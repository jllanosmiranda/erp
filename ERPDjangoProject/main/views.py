from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def redirect_to_home(request):
    return redirect('/home')

@login_required
def home(request):
    return render(request,'main/index.html')