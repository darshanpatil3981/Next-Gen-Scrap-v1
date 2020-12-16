from django.shortcuts import render

# Create your views here.
def Showhome(request):
    return render(request,"app/base.html")

def Login(request):
    return render(request,"app/login.html")

def Register(request):
    return render(request,"app/register.html")