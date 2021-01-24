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

def Signup_customer(request):
    return render(request,"app/signup_customer.html")

def Signup_GCRC(request):
    return render(request,"app/signup_gcrc.html")

def Otp_verification(request):
    return render(request,"app/otp_verification.html")



# ====================================Processing Views=================================================

def Enter_email(request):
    role = request.POST['roleh']
    if role == "customer":
        return render(request,"app/enter_email.html",{'role':role})
    elif role == "business":
        return render(request,"app/enter_email.html",{'role':role})


def is_already_created(request):
    role = request.POST['roleh']
    email = request.POST['email']
    if role=="customer":
        isCustomerAlready = User_Master.objects.filter(Email=email)
        if isCustomerAlready:
            obj = User_Master.objects.get(Email=email)
            err_role= obj.Role
            message = "This email address is already registered as "+err_role+"!"
            return render(request,"app/enter_email.html",{'error':message,'role':role})
        else:
            otp = randint(100000,999999)
            email_Subject = "Customer Email Verification"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear customer','otp':otp})
            return render(request,"app/otp_verification.html",{'OTP':otp,'EMAIL':email,'ROLE':"Customer"})

    elif role == "business":
        isGCRCAlready = User_Master.objects.filter(Email=email)
        if isGCRCAlready:
            obj = User_Master.objects.get(Email=email)
            err_role= obj.Role
            message = "This email address is already registered as "+err_role+"!"
            return render(request,"app/enter_email.html",{'error':message,'role':role})
        else:
            otp = randint(100000,999999)
            email_Subject = "Business Partner Email Verification"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear Business Partner','otp':otp})
            return render(request,"app/otp_verification.html",{'OTP':otp,'EMAIL':email,'ROLE':"GCRC"})
        

def verify_OTP(request):
    cotp = request.POST['cotp']
    otp = request.POST['otp']
    email = request.POST['email']
    role = request.POST['role']
    otp = str(otp)
    cotp = str(cotp)
   
    if otp==cotp:
        if role=="Customer":
            return render(request,"app/signup_customer.html",{'EMAIL':email})
        else:
            return render(request,"app/signup_gcrc.html",{'EMAIL':email})
    else:
        message="You have entered incorrect OTP."
        return render(request,"app/otp_verification.html",{'msg':message,'OTP':otp})



def create_Customer(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    pswd = request.POST['pswd']
    cpswd = request.POST['cpswd']

    if fname=="" or lname=="" or email=="" or pswd=="" or cpswd=="":
            message = "Please fill all details carefully..." 
            return render(request,"app/signup_customer.html",{'msg':message,'EMAIL':email})
    
    elif fname!="" or lname!="" or email!="" or pswd!="" or cpswd!="":      
            if pswd==cpswd:
                newUser = User_Master.objects.create(Email=email,Password=pswd,Role="Customer",Otp=12345,is_created=True,is_verified=False,is_active=False,is_updated=False)
                newCustomer = Customer.objects.create(Customer_ID=newUser,Firstname=fname,Lastname=lname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
                return render(request,"app/index.html")
            else:
                message = "Password Doesnot match"
                return render(request,"app/signup_customer.html",{'msg':message,'EMAIL':email})


def create_gc_rc(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    pswd = request.POST['pass']
    cpswd = request.POST['cpass']
    role = request.POST['role']

    if role == "Srap Collector":
        role="GC"
    elif role == "Recycle Company":
        role="RC"
    
    if fname=="" or lname=="" or email=="" or pswd=="" or cpswd=="":
        message = "Please fill all details carefully..." 
        return render(request,"app/signup_gcrc.html",{'msg':message})
    elif fname!="" or lname!="" or email!="" or pswd!="" or cpswd!="":
        if pswd==cpswd:
            newUser = User_Master.objects.create(Email=email,Password=pswd,Role=role,Otp=12345,is_created=True,is_verified=False,is_active=False,is_updated=False)
            if role=="GC":
                newsc = GC.objects.create(GC_ID=newUser,Firstname=fname,Lastname=lname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
            if role=="RC":
                newrc = RC.objects.create(RC_ID=newUser,Firstname=fname,Lastname=lname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
            return render(request,"app/index.html")
        else:
                message = "Password Doesnot match"
                return render(request,"app/signup_gcrc.html",{'msg':message,'EMAIL':email})


def Validate_login(request):
    email = request.POST['email']
    password = request.POST['password']

    is_exist = User_Master.objects.filter(Email=email,Password=password)

    if is_exist:
        User = User_Master.objects.get(Email=email)
        print(User.Role)
        if User.Role=="Customer":
            return render(request,"app/index.html")
        elif User.Role=="GC":
            return render(request,"app/gc_dashboard.html")
        elif User.Role=="RC":
            return render(request,"app/rc_dashboard.html")
    else:
        message = "Invalide Email Id & Password!!"
        return render(request,"app/login.html",{'msg':message,})

def Forgot_password(request):
    if request.method=="POST":
        email = request.POST['email']
        is_exist = User_Master.objects.filter(Email=email)
        if is_exist:
            otp = randint(100000,999999)
            email_Subject = "Email Verification For Forgot Password"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear customer','otp':otp})
            return render(request,"app/otp_verification.html",{'fpw':"fpw",'OTP':otp,"EMAIL":email})
        else:
            message = "This email is not registed With any account!!"
            return render(request,"app/enter_email.html",{'error':message,'fpw':"fpw"})
    else:
        return render(request,"app/enter_email.html",{'fpw':"fpw",})


def Verify_OTP_forgotpw(request): 
    cotp = request.POST['cotp']
    otp = request.POST['otp']
    email = request.POST['email']
    role = request.POST['role']
    otp = str(otp)
    cotp = str(cotp)
    if otp==cotp:
         return render(request,"app/reset_password.html",{'EMAIL':email})
    else:
        message="You have entered incorrect OTP."
        return render(request,"app/otp_verification.html",{'fpw':"fpw",'msg':message,'OTP':otp,"EMAIL":email})

def Reset_password(request):  
    email = request.POST['email'] 
    password=request.POST['password']
    User = User_Master.objects.get(Email=email)
    User.Password=password
    User.save()
    message = "Your Password Chnaged successfully"
    return render(request,"app/login.html",{'msg':message})



def temp(request):
    return render(request,"app/gc.html")