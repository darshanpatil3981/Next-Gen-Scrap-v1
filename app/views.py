from django.shortcuts import render

# Create your views here.
def Showhome(request):
    return render(request,"app/base.html")

def Login(request):
    return render(request,"app/login.html")

def Signin_customer(request):
    return render(request,"app/signin_customer.html")

def Signin(request):
    return render(request,"app/signin.html")

def Otp_verification(request):
    return render(request,"app/otp_verification.html")