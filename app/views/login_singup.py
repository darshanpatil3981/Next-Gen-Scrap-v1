from django.shortcuts import render,HttpResponseRedirect,reverse,redirect
from ..models import *
from random import *
from ..utils import *
from django.contrib.auth.hashers import make_password,check_password
from itertools import chain
import razorpay
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.http import JsonResponse



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

def Enter_email(request):
    role = request.POST['roleh']
    if role == "customer":
        return render(request,"app/enter_email.html",{'role':role})
    elif role == "business":
        return render(request,"app/enter_email.html",{'role':role})

def Forgot_password(request):
    if request.method=="POST":
        email = request.POST['email']
        is_exist = User_Master.objects.filter(Email=email)
        if is_exist:
            otp = randint(100000,999999)
            encrypted_otp=make_password(otp)
            print(otp)
            email_Subject = "Email Verification For Forgot Password"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear customer','otp':otp})
            return render(request,"app/otp_verification.html",{'fpw':"fpw",'OTP':encrypted_otp,"EMAIL":email})
        else:
            message = "This email is not registed With any account!!"
            return render(request,"app/enter_email.html",{'error':message,'fpw':"fpw"})
    else:
        return render(request,"app/enter_email.html",{'fpw':"fpw",})


def is_already_created(request):
    role = request.POST['roleh']
    email = request.POST.get('email', False)
    if role=="customer":
        isCustomerAlready = User_Master.objects.filter(Email=email)
        if isCustomerAlready:
            obj = User_Master.objects.get(Email=email)
            err_role= obj.Role
            message = "This Email Address Is Already Registered As "+err_role+"!"
            return render(request,"app/enter_email.html",{'error':message,'role':role})
        else:
            otp = randint(100000,999999)
            print(otp)
            encrypted_otp=make_password(otp)
            email_Subject = "Customer Email Verification"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear customer','otp':otp})
            oc_msg = "OTP Sent On "+email+"  Please Verify OTP"
            return render(request,"app/otp_verification.html",{'OTP':encrypted_otp,'EMAIL':email,'ROLE':"Customer",'msg':oc_msg})

    elif role == "business":
        isGCRCAlready = User_Master.objects.filter(Email=email)
        if isGCRCAlready:
            obj = User_Master.objects.get(Email=email)
            err_role= obj.Role
            message = "This Email Address Is Already Registered As "+err_role+"!"
            return render(request,"app/enter_email.html",{'error':message,'role':role})
        else:
            otp = randint(100000,999999)
            print(otp)
            encrypted_otp=make_password(otp)
            email_Subject = "Business Partner Email Verification"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear Business Partner','otp':otp})
            oc_msg = "OTP Sent On "+email+"  Please Verify OTP"
            return render(request,"app/otp_verification.html",{'OTP':encrypted_otp,'EMAIL':email,'ROLE':"GCRC",'msg':oc_msg})
        

def verify_OTP(request):
    cotp = request.POST['cotp']
    otp = request.POST['otp']
    email = request.POST['email']
    role = request.POST['role']
    
    if check_password(cotp,otp):
        success_message = "OTP Is Verified Successfully"
        if role=="Customer":
            return render(request,"app/signup_customer.html",{'EMAIL':email,'msg':success_message})
        else:
            return render(request,"app/signup_gcrc.html",{'EMAIL':email,'msg':success_message})
    else:
        message="Incorrect OTP!!"
        return render(request,"app/otp_verification.html",{'msg':message,'OTP':otp,'EMAIL':email})



def create_Customer(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST.get('email', False)
    pswd = request.POST['pswd']
    cpswd = request.POST['cpswd'] 
    if fname!="" or lname!="" or email!="" or pswd!="" or cpswd!="":      
            if pswd==cpswd:
                encrypted_pw=make_password(pswd)
                newUser = User_Master.objects.create(Email=email,Password=encrypted_pw,Role="Customer",is_created=True,is_verified=False,is_active=False)
                newCustomer = Customer.objects.create(User_Master=newUser,Firstname=fname,Lastname=lname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
                return render(request,"app/login.html")
            else:
                message = "Password Does Not Match"
                return render(request,"app/signup_customer.html",{'fname':fname,'lname':lname,'pswd':pswd,'msg':message,'EMAIL':email})

#done
def create_gc_rc(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST.get('email', False)
    pswd = request.POST['pass']
    cpswd = request.POST['cpass']
    role = request.POST['role']
    cname = request.POST['cname']

    if role == "Srap Collector":
        role="SC"
    elif role == "Recycle Company":
        role="RC"
    
    if fname!="" or lname!="" or email!="" or pswd!="" or cpswd!="":
        if pswd==cpswd:
            encrypted_pw=make_password(pswd)
            newUser = User_Master.objects.create(Email=email,Password=encrypted_pw,Role=role,is_created=True,is_verified=False,is_active=False)
            if role=="SC":
                newsc = SC.objects.create(User_Master=newUser,Firstname=fname,Lastname=lname,Shop_name=cname,Address="",City="",State="",Pincode=000000,Contact=0)
            if role=="RC":
                newrc = RC.objects.create(User_Master=newUser,Firstname=fname,Lastname=lname,Company_name=cname,Address="",City="",State="",Pincode=000000,Contact=0)
            # return render(request,"app/index.html")
            return HttpResponseRedirect(reverse('login'))
        else:
                message = "Password Does Not Match"
                return render(request,"app/signup_gcrc.html",{'fname':fname,'lname':lname,'pswd':pswd,'msg':message,'EMAIL':email})

#done
def Validate_login(request):
    email = request.POST['email']
    password = request.POST['password']
    is_exist = User_Master.objects.filter(Email=email)
    is_admin = Admin.objects.filter(User_Name=email)
    if is_admin:
        admin = Admin.objects.get(User_Name=email)
        
        if(password==admin.Password):
            return redirect('ngs_admin')
        else:
            message = "Incorect Password Of Admin"
            return render(request,"app/login.html",{'msg':message,})
    if is_exist:
        User = User_Master.objects.get(Email=email)
        if check_password(password,User.Password):
            if User.Role=="Customer":
                request.session['id'] = User.id
                customer=Customer.objects.get(User_Master=User)
                request.session['fname']=customer.Firstname
                request.session['lname']=customer.Lastname
               
                
                user = User_Master.objects.get(id=User.id)
                customer = Customer.objects.get(User_Master=user)
                cart_items = Cust_Cart.objects.filter(Customer=customer)
                cart_badge = 0
                for i in cart_items:
                    cart_badge = cart_badge + 1
                request.session['cart_items'] = cart_badge

                return HttpResponseRedirect(reverse('index'))
            elif User.Role=="SC":
                request.session['id']=User.id
                sc=SC.objects.get(User_Master=User)
                request.session['scid']=sc.id
                request.session['fname']=sc.Firstname
                request.session['lname']=sc.Lastname
                request.session['pic']=sc.Profile_Pic.url
                request.session['is_verified']=User.is_verified


               
                try:
                    subscription = Subscription.objects.get(User=User)
                    today_date = datetime.now().date()
                    end_date = subscription.Subscription_Ending_Date
                    if(today_date>end_date):
                        subscription.Is_Active=False
                        sc.Is_Subscription_Active = False
                        sc.save()
                        subscription.save()

                        
                except:
                    pass
                return redirect('sc_scrap_sock')
            elif User.Role=="RC":
                request.session['id']=User.id
                rc=RC.objects.get(User_Master=User)
                request.session['rcid']=rc.id
                request.session['fname']=rc.Firstname
                request.session['lname']=rc.Lastname
                request.session['pic']=rc.Profile_Pic.url
                request.session['is_verified']=User.is_verified


                try:
                    subscription = Subscription.objects.get(User=User)
                    today_date = datetime.now().date()
                    end_date = subscription.Subscription_Ending_Date
                    if(today_date>end_date):
                        subscription.Is_Active=False
                        sc.Is_Subscription_Active = False
                        sc.save()
                        subscription.save()
                except:
                    pass
                
                return redirect('rc_purchase_scrap')
        else:
            message = "Incorect Password!!"
            return render(request,"app/login.html",{'msg':message,})        
    else:
        message = "This Email Is Not Registed with Any Account"
        return render(request,"app/login.html",{'msg':message,})
#done


#done
def Verify_OTP_forgotpw(request): 
    cotp = request.POST['cotp']
    otp = request.POST['otp']
    email = request.POST['email']
    role = request.POST['role']
    otp = str(otp)
    cotp = str(cotp)
    print(otp)
    if check_password(cotp,otp):
         return render(request,"app/reset_password.html",{'EMAIL':email})
    else:
        message="You have entered incorrect OTP."
        return render(request,"app/otp_verification.html",{'fpw':"fpw",'msg':message,'OTP':otp,"EMAIL":email})
#done
def Reset_password(request):  
    email = request.POST['email'] 
    password=request.POST['password']
    User = User_Master.objects.get(Email=email)
    encrypted_pw=make_password(password)
    User.Password=encrypted_pw
    User.save()
    message = "Your Password Chnaged successfully"
    return render(request,"app/login.html",{'msg':message})
