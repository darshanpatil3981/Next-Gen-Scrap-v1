from django.shortcuts import render,HttpResponseRedirect,reverse
from .models import *
from random import *
from .utils import *

# Create your views here.
#def Showhome(request):
#    return render(request,"app/base.html")

def Login_Page(request):
    return render(request,"app/login.html")

def Signup_customer(request):
    return render(request,"app/signup_customer.html")

def Signup_RCGC(request):
    return render(request,"app/signup_gcrc.html")

def Otp_verification(request):
    return render(request,"app/otp_verification.html")


#======================================================================================


def create_Customer(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    pswd = request.POST['pswd']
    cpswd = request.POST['cpswd']

    if fname=="" or lname=="" or email=="" or pswd=="" or cpswd=="":
            message = "Please fill all details carefully..." 
            return render(request,"app/signup_customer.html",{'msg':message})
    
    elif fname!="" or lname!="" or email!="" or pswd!="" or cpswd!="":
        isCraeatedAlready = User_Master.objects.filter(Email=email)
        if isCraeatedAlready:
            message = "This acoount is already created"
            return render(request,"app/signup_customer.html",{'msg':message})

        elif pswd==cpswd:
                otp = randint(100000,999999)
                newUser = User_Master.objects.create(Email=email,Password=pswd,Role="Customer",Otp=otp,is_created=True,is_verified=False,is_active=False,is_updated=False)
                newCustomer = Customer.objects.create(Customer_ID=newUser,Firstname=fname,Lastname=lname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
                email_Subject = "Customer Verification Mail"
                sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':fname,'otp':otp})
                return render(request,"app/otp_verification.html")
        else:
            message = "Password Doesnot match"
            return render(request,"app/signup_customer.html",{'msg':message})

