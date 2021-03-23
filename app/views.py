from django.shortcuts import render,HttpResponseRedirect,reverse,redirect
from .models import *
from random import *
from .utils import *
from django.contrib.auth.hashers import make_password,check_password
from itertools import chain
import razorpay
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import datetime, timedelta



from django.conf import settings 
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
                newUser = User_Master.objects.create(Email=email,Password=encrypted_pw,Role="Customer",is_created=True,is_verified=False,is_active=False,is_updated=False)
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
            newUser = User_Master.objects.create(Email=email,Password=encrypted_pw,Role=role,is_created=True,is_verified=False,is_active=False,is_updated=False)
            if role=="SC":
                newsc = SC.objects.create(User_Master=newUser,Firstname=fname,Lastname=lname,Shop_name=cname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
            if role=="RC":
                newrc = RC.objects.create(User_Master=newUser,Firstname=fname,Lastname=lname,Company_name=cname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
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
        print(admin)
        if(password==admin.Password):
            return redirect('ngs_admin')
        else:
            message = "Incorect Password Of Admin"
            return render(request,"app/login.html",{'msg':message,})
    if is_exist:
        User = User_Master.objects.get(Email=email)
        if check_password(password,User.Password):
            if User.Role=="Customer":
                request.session['id']=User.id
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

               
                try:
                    subscription = Subscription.objects.get(User=User)
                    today_date = datetime.now().date()
                    end_date = subscription.Subscription_Ending_Date
                    if(today_date>end_date):
                        subscription.Is_Active=False
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
                try:
                    subscription = Subscription.objects.get(User=User)
                    today_date = datetime.now().date()
                    end_date = subscription.Subscription_Ending_Date
                    if(today_date>end_date):
                        subscription.Is_Active=False
                        subscription.save()
                except:
                    pass
                
                return redirect('rc_scrap_collectors')
        else:
            message = "Incorect Password!!"
            return render(request,"app/login.html",{'msg':message,})        
    else:
        message = "This Email Is Not Registed with Any Account"
        return render(request,"app/login.html",{'msg':message,})
#done
def Forgot_password(request):
    if request.method=="POST":
        email = request.POST['email']
        is_exist = User_Master.objects.filter(Email=email)
        if is_exist:
            otp = randint(100000,999999)
            encrypted_otp=make_password(otp)
            email_Subject = "Email Verification For Forgot Password"
            sendmail(email_Subject,'otpVerification_emailTemplate',email,{'name':'Dear customer','otp':otp})
            return render(request,"app/otp_verification.html",{'fpw':"fpw",'OTP':encrypted_otp,"EMAIL":email})
        else:
            message = "This email is not registed With any account!!"
            return render(request,"app/enter_email.html",{'error':message,'fpw':"fpw"})
    else:
        return render(request,"app/enter_email.html",{'fpw':"fpw",})

#done
def Verify_OTP_forgotpw(request): 
    cotp = request.POST['cotp']
    otp = request.POST['otp']
    email = request.POST['email']
    role = request.POST['role']
    otp = str(otp)
    cotp = str(cotp)
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



def Rc_scrap_collectors(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)
    sc=SC.objects.all()
    print(sc)
    return render(request,"rc/rc_scrap_collectors.html",{'user':user,'rc':rc,'sc':sc})


def View_Sc_Profile(request,key):
    sc=SC.objects.get(id=key)
    return render(request,"rc/sc_profile.html",{'sc':sc})
    

def Rc_blank(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)
    return render(request,"rc/rc_blank.html",{'user':user,'rc':rc})


def Rc_profile(request):
    id=request.session.get("id")
    user=User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)
    return render(request,"rc/rc_profile.html",{'user':user,'rc':rc})



def Rc_update_profile(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        add = request.POST['add']
        contact = request.POST['contact']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc=RC.objects.get(User_Master=user)
        rc.Firstname=fname
        rc.Lastname=lname
        rc.Address=add
        rc.Contact=contact
        rc.City=city
        rc.State=state
        rc.Pincode=pincode
        try:
            if request.FILES['profile_pic']:
                propic = request.FILES['profile_pic']
                rc.Profile_Pic=propic
                rc.save()
        except:
            rc.save()

        return HttpResponseRedirect(reverse('rc_profile'))
    else:
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc=RC.objects.get(User_Master=user)
        return render(request,"rc/rc_update_profile.html",{'user':user,'rc':rc})
    

def Rc_orders(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)
    order_product =  Product_Order.objects.filter(RC_ID=rc.id,Payment_status="Success")
    return render(request,"rc/rc_orders.html",{'user':user,'rc':rc,'order_product':order_product})

def Rc_pricing(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)
    try:
        subscription = Subscription.objects.get(User=user)
        return render(request,"rc/rc_pricing.html",{'user':user,'rc':rc,'subscription':subscription})
    except:
        return render(request,"rc/rc_pricing.html",{'user':user,'rc':rc})

def Rc_product(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)
    products=Product.objects.all().filter(RC=rc)
    return render(request,"rc/rc_product.html",{'user':user,'rc':rc,'products':products})



def Rc_add_product(request):
    if request.method=="POST":
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc = RC.objects.get(User_Master=user)

        pro_name = request.POST['Pro_name']
        pro_price = request.POST['Pro_price']
        pro_desc = request.POST['Pro_desc']
        pro_img = request.FILES['Pro_img']
        seller_name=rc.Firstname+" "+rc.Lastname

        newProduct = Product.objects.create(RC=rc,Seller_Name=seller_name,Product_Name=pro_name,Product_Price=pro_price,Product_Desc=pro_desc,Product_Img=pro_img,Current_orders=0)
        return HttpResponseRedirect(reverse('rc_product'))
    else:
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc=RC.objects.get(User_Master=user)
        return render(request,"rc/rc_add_product.html",{'user':user,'rc':rc})



def RC_view_product(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc = RC.objects.get(User_Master=user)
    product = Product.objects.get(id=key)
    return render(request,"rc/rc_view_product.html",{'user':user,'rc':rc,'product':product})


def RC_edit_product(request,key):
    if request.method=="POST":
        pro_name = request.POST['Pro_name']
        pro_price = request.POST['Pro_price']
        pro_desc = request.POST['Pro_desc']
        
        product = Product.objects.get(id=key)
        product.Product_Name = pro_name
        product.Product_Price = pro_price
        product.Product_Desc = pro_desc
        try:
            if request.FILES['Pro_img']:
                pro_img = request.FILES['Pro_img']
                product.Product_Img = pro_img
                product.save()    
        except:
            product.save()

        id = request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc = RC.objects.get(User_Master=user)
        # return HttpResponseRedirect(reverse('RC_view_product',args={'key':product.id}))
        return HttpResponseRedirect(reverse('RC_view_product',args=[product.id]))

    else:
        id = request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc = RC.objects.get(User_Master=user)
        product = Product.objects.get(id=key)
        return render(request,"rc/rc_edit_product.html",{'user':user,'rc':rc,'product':product})


def RC_delete_product(request,key):
    delProduct = Product.objects.get(id=key)
    if(delProduct.Product_Img):
       delProduct.Product_Img.delete()
    delProduct.delete()
    return HttpResponseRedirect(reverse("rc_product"))


def Rc_change_password(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)

    if request.method=="POST":
        old_password = request.POST['op']
        new_password = request.POST['np']
        confirm_password= request.POST['cp']

        if check_password(old_password,user.Password):
            if new_password==confirm_password:
                encrypted_pw=make_password(new_password)
                user.Password=encrypted_pw
                user.save()
                msg="Your Password Changed Succsessfully!!!"
                return render(request,"rc/rc_change_password.html",{'user':user,'rc':rc,'msg':msg})
            else:
                msg="New Password & Confirm Password Did Not Match!!!"
                return render(request,"rc/rc_change_password.html",{'user':user,'rc':rc,'msg':msg})
        else:
            msg="Old Password Is Incorect!!!"
            return render(request,"rc/rc_change_password.html",{'user':user,'rc':rc,'msg':msg})
    else:
        return render(request,"rc/rc_change_password.html",{'user':user,'rc':rc})


def Subscription_detail(request):
    if 'personal' in request.POST: 
        subscription_name = "Personal"
        subscription__duration = "30 Days"
        starting_date = datetime.now().date()
        ending_date = starting_date+timedelta(days=30)
        total_amount = 100
    elif 'professional' in request.POST: 
        subscription_name = "Professional"
        subscription__duration = "184 Days"
        starting_date = datetime.now().date()
        ending_date = starting_date+timedelta(days=184)
        total_amount = 600
    elif 'enterprise' in request.POST: 
        subscription_name = "Enterprise"
        subscription__duration = "365 Days"
        starting_date = datetime.now().date()
        ending_date = starting_date+timedelta(days=365)
        total_amount = 1200

    id=request.session.get("id")
    user = User_Master.objects.get(id=id)


    client = razorpay.Client(auth=('rzp_test_UtV7JVYk3ROncb','cgjsHRXA0c7HCFzyDfrZoel4'))
    payment = client.order.create({'amount': total_amount*100, 'currency': 'INR','payment_capture': '1',})   
    invoice_no = randint(1000000,9999999)
    try:
        subscription = Subscription.objects.get(User=user)
        subscription.Subscription_Name=subscription_name
        subscription.Subscription_Amount=total_amount
        subscription.Subscription_Starting_Date=starting_date
        subscription.Subscription_Ending_Date=ending_date
        subscription.save()
        request.session['subscription_id']=subscription.id
    except:
        new_subscription = Subscription.objects.create(User=user,
                                                       Role = user.Role, 
                                                       Is_Active=False,
                                                       Subscription_Name=subscription_name,
                                                       Subscription_Amount=total_amount,
                                                       Subscription_Starting_Date=starting_date,
                                                       Subscription_Ending_Date=ending_date,
                                                       Invoice_No=invoice_no,
                                                       Razorpay_order_id="",
                                                       Razorpay_payment_id="",
                                                       razorpay_signature="",
                                                       )
        request.session['subscription_id']=new_subscription.id
    if(user.Role=='RC'):
        rc=RC.objects.get(User_Master=user)
        return render(request,"rc/Subscription_detail.html",{'payment':payment,'subscription_name':subscription_name,'subscription__duration':subscription__duration,'starting_date':starting_date,'ending_date':ending_date,'amount':total_amount,'total_amount':total_amount,'rc':rc,'user':user})
    elif(user.Role=="SC"):
        sc=SC.objects.get(User_Master=user)
        return render(request,"sc/Subscription_detail.html",{'payment':payment,'subscription_name':subscription_name,'subscription__duration':subscription__duration,'starting_date':starting_date,'ending_date':ending_date,'amount':total_amount,'total_amount':total_amount,'sc':sc,'user':user})


@csrf_exempt
def Invoice_Subscription(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    response=request.POST
    subscription_id=request.session.get("subscription_id")
    verification = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    subscription = Subscription.objects.get(id=subscription_id)
       
   
    client = razorpay.Client(auth=('rzp_test_UtV7JVYk3ROncb','cgjsHRXA0c7HCFzyDfrZoel4'))
    try:
        status = client.utility.verify_payment_signature(verification)
        subscription.Is_Active=True
        subscription.Razorpay_order_id = response['razorpay_order_id']
        subscription.Razorpay_payment_id = response['razorpay_payment_id']
        subscription.razorpay_signature =  response['razorpay_signature']
        subscription.save()
        email = user.Email
        email_Subject = "Your Subscription Activated"
        if(user.Role=='RC'):
            rc=RC.objects.get(User_Master=user)
            sendmail_invoice_subscription(email_Subject,'invoice_subscription_email',email,{'subscription':subscription,'rc':rc,'user':user}) 
            return render(request,"rc/invoice_subscription.html",{'subscription':subscription,'rc':rc,'user':user})

        elif(user.Role=="SC"):
            sc=SC.objects.get(User_Master=user)
            sendmail_invoice_subscription_sc(email_Subject,'invoice_subscription_email',email,{'subscription':subscription,'sc':sc,'user':user})
            return render(request,"sc/invoice_subscription.html",{'subscription':subscription,'sc':sc,'user':user})
    except:
        print("Filed")
        return render(request,"rc/invoice_subscription.html",)

def Invoice_Sub_Pdf(request,key):
    subscription = Subscription.objects.get(id=key)
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    if(user.Role=='RC'):    
        rc=RC.objects.get(User_Master=user)
        data = {
                'subscription':subscription,
                'rc':rc,
                'user':user
        }
    elif(user.Role=="SC"):
        sc=SC.objects.get(User_Master=user)
        data = {
                'subscription':subscription,
                'sc':sc,
                'user':user
        }
    pdf = render_to_pdf('rc/invoice_subscription.html',data)
    return HttpResponse(pdf, content_type='application/pdf')

#Done
def Index(request):
    products = Product.objects.all()
    return render(request,"ecom/index.html",{'products':products})
 #Done   
def Product_detail(request,key):
    product = Product.objects.get(pk=key)
    comments = Ecom_comments.objects.filter(Product=product)
    return render(request,"ecom/product_detail.html",{'product':product,'comments':comments})
#Done
def Profile(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    return render(request,"ecom/profile.html",{'user':user,'customer':customer})
#Done
def Logout(request):
    try:
        del request.session['id']
        del request.session['fname']
        del request.session['lname']
        del request.session['cart_items']
        return HttpResponseRedirect(reverse('login'))
    except:
        return HttpResponseRedirect(reverse('login'))

#Done
def Customer_update_profile(request):
    if request.method=="POST":
        id = request.session.get("id")
        user = User_Master.objects.get(id=id)
        customer=Customer.objects.get(User_Master=user)
        customer.Firstname=request.POST['fname']
        customer.Lastname=request.POST['lname']
        customer.Address=request.POST['add']
        customer.Contact=request.POST['contact']
        customer.City=request.POST['city']
        customer.State=request.POST['state']
        customer.Pincode=request.POST['pincode']
        try:
            if request.FILES['profile_pic']:
                propic = request.FILES['profile_pic']
                customer.Profile_Pic=propic
                customer.save()
        except:
            customer.save()

        return HttpResponseRedirect(reverse('profile'))
    else:
        id = request.session.get("id")
        user = User_Master.objects.get(id=id)
        customer=Customer.objects.get(User_Master=user)
        return render(request,"ecom/customer_update_profile.html",{'user':user,'customer':customer})
#done
def Change_password(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    if request.method=="POST":
        old_password = request.POST['op']
        new_password = request.POST['np']
        confirm_password= request.POST['cp']
      
        if check_password(old_password,user.Password):
            if new_password==confirm_password:
                encrypted_pw=make_password(new_password)
                user.Password=encrypted_pw
                user.save()
                msg="Your Password Changed Succsessfully!!!"
                return render(request,"ecom/change_password.html",{'msg':msg})
            else:
                msg="New Password & Confirm Password Did Not Match!!!"
                return render(request,"ecom/change_password.html",{'msg':msg})
        else:
            msg="Old Password Is Incorect!!!"
            return render(request,"ecom/change_password.html",{'msg':msg})
    else:
        return render(request,"ecom/change_password.html")
    
#done
def add_to_cart_or_buy_now(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer = Customer.objects.get(User_Master=user)
    product = Product.objects.get(id=key)
    quantity = request.POST['quantity_copy']

    if 'add_to_cart' in request.POST:
        per_pro_price = product.Product_Price
        total_amt = int(quantity)*int(per_pro_price)
        new_cart_item = Cust_Cart.objects.create(Customer=customer,Product=product,Quantity=quantity,Total_Amount=total_amt)
        # AHI "ITEM ADDED TO CART SUCCESSFULLY NO MESSAGE FIRE KARAVO CHE... EK MESSAGE LAI RENDER MA PASS KARVO PADE"
        # PN RENDER MA PASS KARE TYARE PRODUCT na OBJECTS.ALL() KARI MOKALJE NAI TO ERROR MARSE
        # return render(request,"ecom/index.html",{'user':user,'customer':customer,'products':product})
        cart_i_up = int(request.session['cart_items']) + 1
        request.session['cart_items'] = cart_i_up
        return HttpResponseRedirect(reverse('product_detail',args=[product.id]))

    elif 'buy_now' in request.POST:
        per_pro_price = product.Product_Price
        total_amt = int(quantity)*int(per_pro_price)
        total = total_amt + 40
        new_cart_item = Cust_Cart.objects.create(Customer=customer,Product=product,Quantity=quantity,Total_Amount=total_amt)
        cart_i_up = int(request.session['cart_items']) + 1
        request.session['cart_items'] = cart_i_up
        return render(request,"ecom/checkout.html",{'new_cart_item':new_cart_item,'item':quantity,'sub_total':total_amt,'total':total})
        # return HttpResponseRedirect(reverse('checkout'))


#done
def Cart(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    cust_cart = Cust_Cart.objects.filter(Customer=customer)
    return render(request,"ecom/cart.html",{'cust_cart':cust_cart})
    
#done
def edit_order(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    item = Cust_Cart.objects.get(id=key)
    
    if 'update_plus' in request.POST:
        new_quant = int(item.Quantity) + 1
        item.Quantity = new_quant
        item.Total_Amount = item.Product.Product_Price * item.Quantity
        item.save()
    
    if 'update_minus' in request.POST:
        new_quant = int(item.Quantity) - 1
        item.Quantity = new_quant
        item.Total_Amount = item.Product.Product_Price * item.Quantity
        item.save()
    
    return HttpResponseRedirect(reverse("cart"))
#done
def remove_cart_item(request,key):
    id = request.session.get("id")
    item = Cust_Cart.objects.get(id=key)
    item.delete()
    cart_i_up = int(request.session['cart_items']) - 1
    request.session['cart_items'] = cart_i_up
    return HttpResponseRedirect(reverse("cart"))


def Checkout(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)

    cust_cart = Cust_Cart.objects.filter(Customer=customer)
    item=0
    sub_total=0
    for i in cust_cart:
        item=item+i.Quantity
        sub_total=sub_total+i.Total_Amount
    total=sub_total+40 
    return render(request,"ecom/checkout.html",{'cust_cart':cust_cart,'item':item,'sub_total':sub_total,'total':total})


def Shipping_detail(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
  
    if 'Single' in request.POST:
        product_id = request.POST['product_id']
        product_quantity = request.POST['product_quantity']
        product_price = int(request.POST['total'])
        cart_id = request.POST['cart_id']
        item = Cust_Cart.objects.get(id=cart_id)
        item.delete()
        cart_i_up = int(request.session['cart_items']) - 1
        request.session['cart_items'] = cart_i_up
        product = Product.objects.get(id=product_id)
        order_id=uuid.uuid4()
        amount = product_price
        rc = RC.objects.get(id = product.RC.id)
        product_Order_price = amount-40
        
        client = razorpay.Client(auth=('rzp_test_UtV7JVYk3ROncb','cgjsHRXA0c7HCFzyDfrZoel4'))
        payment = client.order.create({'amount': amount*100, 'currency': 'INR','payment_capture': '1',})   
        invoice_no = randint(1000000,9999999)
        sub_total = product_price-40
        new_order = Order.objects.create(Order_id=order_id,Customer=customer,Total_Amount=product_price,Sub_Total_Amount=sub_total,Payment_status="panding",Razorpay_order_id="",Razorpay_payment_id="",Invoice_No=invoice_no)
   

        new_product_Order = Product_Order.objects.create(Order=new_order,Product=product,Quantity=product_quantity,Price=product_Order_price,RC_ID=rc.id,Customer = customer.id)
        
        request.session['order_id']=new_order.id
        return render(request,"ecom/shipping_detail.html",{'user':user,'customer':customer,'payment':payment,'amount':product_price,'order_id':order_id})
 
    if 'Multiple' in request.POST:
        
        cust_cart = Cust_Cart.objects.filter(Customer=customer)
        item=0
        sub_total=0
        for i in cust_cart:
            item=item+i.Quantity
            sub_total=sub_total+i.Total_Amount
       
        total=sub_total+40

        amount = total
        client = razorpay.Client(auth=('rzp_test_UtV7JVYk3ROncb','cgjsHRXA0c7HCFzyDfrZoel4'))
        payment = client.order.create({'amount': amount*100, 'currency': 'INR','payment_capture': '1',})   

        order_id=uuid.uuid4()
        invoice_no = randint(1000000,9999999)
        
      
        new_order = Order.objects.create(Order_id=order_id,Customer=customer,Total_Amount=amount,Sub_Total_Amount=sub_total,Payment_status="panding",Razorpay_order_id="",Razorpay_payment_id="",Invoice_No=invoice_no)
        for i in cust_cart:
            product_Order_price = i.Quantity*i.Product.Product_Price
            Product_Order.objects.create(Order=new_order,Product=i.Product,Quantity=i.Quantity,Price=i.Total_Amount,RC_ID=i.Product.RC.id,Customer = customer.id,Cart_ID=i.id)
        request.session['order_id']=new_order.id
        return render(request,"ecom/shipping_detail.html",{'user':user,'customer':customer,'payment':payment,'amount':amount,'order_id':order_id})
        

@csrf_exempt
def Invoice(request):
    response=request.POST
    order_id=request.session.get("order_id")
    verification = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    order = Order.objects.get(id=order_id)
    product = Product_Order.objects.filter(Order=order)

    email = order.Customer.User_Master.Email
    email_Subject = "Your Order Placed Suscessfully"
    sendmail_invoice(email_Subject,'invoice_email',email,{'order':order,'product':product})    
    order.Payment_status = "Success"
    order.Razorpay_order_id = response['razorpay_order_id']
    order.Razorpay_payment_id = response['razorpay_payment_id']
    date1 = datetime.now().date()
    order.Datetime_of_payment = date1
    order.razorpay_signature =  response['razorpay_signature']
    order.save()
    product_order = Product_Order.objects.filter(Order=order)
    try:
        for i in product_order:
            i.Payment_status="Success"
            i.save()
            item = Cust_Cart.objects.get(id=i.Cart_ID)
            item.delete()
            cart_i_up = int(request.session['cart_items']) - 1
            request.session['cart_items'] = cart_i_up
    except:
         pass
    client = razorpay.Client(auth=('rzp_test_UtV7JVYk3ROncb','cgjsHRXA0c7HCFzyDfrZoel4'))
    try:
        status = client.utility.verify_payment_signature(verification)
        return render(request,"ecom/invoice.html",{'order':order,'product':product})
    except:
        return render(request,"ecom/invoice.html",{'status':status})
def View_Invoice(request,key):
    order = Order.objects.get(id=key)
    product = Product_Order.objects.filter(Order=order)
    return render(request,"ecom/invoice.html",{'order':order,'product':product})

def Customer_orders(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    order = Order.objects.filter(Customer=customer.id,Payment_status="Success")
    # for i in order:
    #      t=i.Datetime_of_payment
    #      print("Before Add")
    #      print(t)
    #      t = t+timedelta(Days=30)
    #      print("After Add")

    #      print(t)
    order_product =  Product_Order.objects.filter(Customer=customer.id,Payment_status="Success")
    return render(request,"ecom/customer_orders.html",{'order_product':order_product,'order':order})

def Customer_orders_detail(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    order_product =  Product_Order.objects.filter(Order=key,Customer=customer.id,Payment_status="Success")
    return render(request,"ecom/customer_orders_detail.html",{'order_product':order_product,})

def Invoice_pdf(request,key):
    order=Order.objects.get(id=key)
    product = Product_Order.objects.filter(Order=order)
    
    data = {
             'order':order,
             'product':product,
        }
    pdf = render_to_pdf('ecom/invoice.html',data)
    return HttpResponse(pdf, content_type='application/pdf')
    
def temp(request):
    return render(request,"rc/temp.html")


def Add_coomment_ecom(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    product = Product.objects.get(id=key)

    print("Got HERE")
    cmt_text = request.POST['cmt_msg']
    cmt_date = datetime.now().date()
    
    cmt_obj = Ecom_comments.objects.create(Product=product,Customer=customer,Comment_text=cmt_text,Comment_time=cmt_date)
    print("Here too")
    return HttpResponseRedirect(reverse('product_detail',args=[product.id]))


#SC Views

def Sc_Profile(request):
    id=request.session.get("id")
    user=User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    return render(request,"sc/sc_profile.html",{'user':user,'sc':sc})

def Sc_Update_Profile(request):
    print("----------------------")
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        add = request.POST['add']
        contact = request.POST['contact']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        print(user)
        sc=SC.objects.get(User_Master=user)
        sc.Firstname=fname
        sc.Lastname=lname
        sc.Address=add
        sc.Contact=contact
        sc.City=city
        sc.State=state
        sc.Pincode=pincode
    
        try:
            if request.FILES['profile_pic']:
                propic = request.FILES['profile_pic']
                sc.Profile_Pic = propic
                sc.save()
        except:
            sc.save()

        return HttpResponseRedirect(reverse('sc_profile'))
    else:
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        sc=SC.objects.get(User_Master=user)
        return render(request,"sc/sc_update_profile.html",{'user':user,'sc':sc})

def Sc_Change_Password(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    print("111111111111111111111")
    if request.method=="POST":
        old_password = request.POST['op']
        new_password = request.POST['np']
        confirm_password= request.POST['cp']
        print("22222222222222222222")
        
        if check_password(old_password,user.Password):
            print("333333333333333333333")
            if new_password==confirm_password:
                encrypted_pw=make_password(new_password)
                user.Password=encrypted_pw
                user.save()
                msg="Your Password Changed Succsessfully!!!"
                return render(request,"sc/sc_change_password.html",{'user':user,'sc':sc,'msg':msg})
            else:
                msg="New Password & Confirm Password Did Not Match!!!"
                return render(request,"sc/sc_change_password.html",{'user':user,'sc':sc,'msg':msg})
        else:
            msg="Old Password Is Incorect!!!"
            return render(request,"sc/sc_change_password.html",{'user':user,'sc':sc,'msg':msg})
    else:
        return render(request,"sc/sc_change_password.html",{'user':user,'sc':sc})
   

def Sc_Pricing(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    try:
        subscription = Subscription.objects.get(User=user)
        return render(request,"sc/sc_pricing.html",{'user':user,'sc':sc,'subscription':subscription})
    except:
        return render(request,"sc/sc_pricing.html",{'user':user,'sc':sc})
    

def Sc_Scrap_Stock(request):
    scrap_categories = Scrap_Categories.objects.all()
    scrap_stock = Scrap_Stock.objects.all()
    return render(request,"sc/sc_scrap_sock.html",{'scrap_categories':scrap_categories,'scrap_stock':scrap_stock})

def Sc_Scrap_Request_Customer(request):
    return render(request,"sc/sc_scrap_request_customer.html")

def Sc_Scrap_Request_Rc(request):
    return render(request,"sc/sc_scrap_request_rc.html")

def Ngs_Admin(request):
    return render(request,"ngs_admin/scrap_categories.html")

def Scrap_Categories1(request):
    scrap_categories = Scrap_Categories.objects.all()
    return render(request,"ngs_admin/scrap_categories.html",{'scrap_categories':scrap_categories})

def Add_Scrap_Categories(request):

    if request.method=="POST":
        name = request.POST['name']
        price = request.POST['price']
        
        try:
            img = request.FILES['img']
            new_scrap = Scrap_Categories.objects.create(Name=name,Price=price,Image=img,)
        except:
            new_scrap = Scrap_Categories.objects.create(Name=name,Price=price)

        return HttpResponseRedirect(reverse('scrap_categories'))
    else:
       return render(request,"ngs_admin/add_scrap_categories.html",)


def Edit_Scrap_Category(request,key):
    cat = Scrap_Categories.objects.get(id=key)
    if request.method=="POST":
        name = request.POST['name']
        price = request.POST['price']
        cat.Name = name
        cat.Price = price
        try:
            img = request.FILES['img']
            cat.Image = img
            cat.save()
        except:
            cat.save()
        return redirect('scrap_categories')
    else:
        return render(request,"ngs_admin/update_scrap_categorie.html",{'cat':cat})

def Delete_Scrap_Category(request,key):
    delcat = Scrap_Categories.objects.get(id=key)
    if(delcat.Image):
       delcat.Image.delete()
    delcat.delete()
    return redirect('scrap_categories')

def Add_Stock(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    cat_name=request.POST['sname']
    cat = Scrap_Categories.objects.get(Name=cat_name)
    print(cat)
    new_scrap = Scrap_Stock.objects.create(Name=cat.Name,Price=cat.Price,Image=cat.Image,In_Stock=True,SC=sc)
    return redirect('sc_scrap_sock')

def Delete_stock(request,key):
    stock = Scrap_Stock.objects.get(id=key)
    if(stock.Image):
       stock.Image.delete()
    stock.delete()
    return redirect('sc_scrap_sock')

def Update_Stock(request,key):
    stock = Scrap_Stock.objects.get(id=key)
    if(stock.In_Stock==True):
        stock.In_Stock=False
    elif(stock.In_Stock==False):
        stock.In_Stock=True
    stock.save()
    return redirect('sc_scrap_sock')


