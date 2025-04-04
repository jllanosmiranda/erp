from django.shortcuts import render, redirect

# Create your views here.
def redirect_to_home(request):
    return redirect('/home')

def home(request):
    return render(request,'main/index.html')