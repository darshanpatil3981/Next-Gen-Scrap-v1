from django.shortcuts import render,HttpResponseRedirect,reverse
from .models import *
from random import *
from .utils import *

# Create your views here.

#==============================Direct Rendering Views================================================
def Login_Page(request):
    return render(request,"app/login.html")

def Signup_as(request):
    return render(request,"app/signup_as.html")

def Enter_email(request):
    role = request.POST['roleh']
    if role == "customer":
        return render(request,"app/enter_email.html",{'role':role})
    elif role == "business":
        return render(request,"app/enter_email.html",{'role':role})

    # if key==1:
    #     message='1'
    # elif key==2:
    #     message='2'
    # else:
    #     message = "Something went wrong."
    # return render(request,"app/enter_email.html",{'msg':message})  

def Signup_customer(request):
    return render(request,"app/signup_customer.html")

def Signup_GCRC(request):
    return render(request,"app/signup_gcrc.html")

def Otp_verification(request):
    return render(request,"app/otp_verification.html")



# ====================================Processing Views=================================================

def is_already_created(request):
    role = request.POST['roleh']
    email = request.POST['email']
    if role=="customer":
        isCustomerAlready = User_Master.objects.filter(Email=email,Role="Customer")
        if isCustomerAlready:
            message = "This email address is already registered as customer."
            return render(request,"app/enter_email.html",{'error':message,'role':role})
        else:
            otp = randint(100000,999999)
            email_Subject = "Customer Email Verification"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear customer','otp':otp})
            return render(request,"app/otp_verification.html",{'OTP':otp,'EMAIL':email,'ROLE':"Customer"})

    elif role == "business":
        isGCRCAlready = User_Master.objects.filter(Email=email,Role="GC")
        isRCAlready = User_Master.objects.filter(Email=email,Role="RC")
        if isGCRCAlready or isRCAlready:
            message = "This email address is already registered as business partner."
            return render(request,"app/enter_email.html",{'error':message,'role':role})
        else:
            otp = randint(100000,999999)
            email_Subject = "Business Partner Email Verification"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear Business Partner','otp':otp})
            return render(request,"app/otp_verification.html",{'OTP':otp,'EMAIL':email,'ROLE':"GCRC"})
        

def verify_OTP(request,sotp):
    cotp = request.POST['cotp']
    email = request.POST['email']
    role = request.POST['role']
    sotp = str(sotp)
    cotp = str(cotp)
    if sotp==cotp:
        if role=="Customer":
            return render(request,"app/signup_customer.html",{'EMAIL':email})
        #if role=="GCRC":
        else:
            return render(request,"app/signup_gcrc.html",{'EMAIL':email})
    else:
        message="You have entered incorrect OTP."
        return render(request,"app/otp_verification.html",{'msg':message,'OTP':sotp})



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
#        isCraeatedAlready = User_Master.objects.filter(Email=email)
#        if isCraeatedAlready:
#            message = "This acoount is already created"
#            return render(request,"app/signup_customer.html",{'msg':message})
#        elif pswd==cpswd:
            if pswd==cpswd:
                #otp = randint(100000,999999)
                newUser = User_Master.objects.create(Email=email,Password=pswd,Role="Customer",Otp=12345,is_created=True,is_verified=False,is_active=False,is_updated=False)
                newCustomer = Customer.objects.create(Customer_ID=newUser,Firstname=fname,Lastname=lname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
                #email_Subject = "Customer Verification Mail"
                #sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':fname,'otp':otp})
                #return render(request,"app/otp_verification.html",{'obj':newUser})
                return render(request,"app/index.html")
            else:
                message = "Password Doesnot match"
                return render(request,"app/signup_customer.html",{'msg':message,'EMAIL':email})



