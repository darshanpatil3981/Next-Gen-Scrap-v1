from django.shortcuts import render,HttpResponseRedirect,reverse
from .models import *
from random import *
from .utils import *
from django.contrib.auth.hashers import make_password,check_password
from itertools import chain
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
    print(otp)
    print(cotp)
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
                newCustomer = Customer.objects.create(Customer_ID=newUser,Firstname=fname,Lastname=lname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
                return render(request,"app/login.html")
            else:
                message = "Password Does Not Match"
                return render(request,"app/signup_customer.html",{'fname':fname,'lname':lname,'pswd':pswd,'msg':message,'EMAIL':email})


def create_gc_rc(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST.get('email', False)
    pswd = request.POST['pass']
    cpswd = request.POST['cpass']
    role = request.POST['role']
    cname = request.POST['cname']

    if role == "Srap Collector":
        role="GC"
    elif role == "Recycle Company":
        role="RC"
    
    if fname!="" or lname!="" or email!="" or pswd!="" or cpswd!="":
        if pswd==cpswd:
            encrypted_pw=make_password(pswd)
            newUser = User_Master.objects.create(Email=email,Password=encrypted_pw,Role=role,is_created=True,is_verified=False,is_active=False,is_updated=False)
            if role=="GC":
                newsc = GC.objects.create(GC_ID=newUser,Firstname=fname,Lastname=lname,Shop_name=cname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
            if role=="RC":
                newrc = RC.objects.create(RC_ID=newUser,Firstname=fname,Lastname=lname,Company_name=cname,Address="",City="",State="",Pincode=000000,Contact=0,Profile_Pic="")
            # return render(request,"app/index.html")
            return HttpResponseRedirect(reverse('login'))
        else:
                message = "Password Does Not Match"
                return render(request,"app/signup_gcrc.html",{'fname':fname,'lname':lname,'pswd':pswd,'msg':message,'EMAIL':email})


def Validate_login(request):
    email = request.POST['email']
    password = request.POST['password']
    
    is_exist = User_Master.objects.filter(Email=email)

    if is_exist:
        User = User_Master.objects.get(Email=email)
        print(check_password(password,User.Password))
        if check_password(password,User.Password):
            if User.Role=="Customer":
                request.session['id']=User.id
                customer=Customer.objects.get(Customer_ID=User)
                request.session['fname']=customer.Firstname
                request.session['lname']=customer.Lastname
                return HttpResponseRedirect(reverse('index'))
            elif User.Role=="GC":
                return render(request,"app/gc_dashboard.html")
            elif User.Role=="RC":
                request.session['id']=User.id
                rc=RC.objects.get(RC_ID=User)
                request.session['rcid']=rc.id
                request.session['fname']=rc.Firstname
                request.session['lname']=rc.Lastname
                return render(request,"rc/rc_dashboard.html",{'user':User,'rc':rc})
        else:
            message = "Incorect Password!!"
            return render(request,"app/login.html",{'msg':message,})        
    else:
        message = "This Email Is Not Registed with Any Account"
        return render(request,"app/login.html",{'msg':message,})

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
    rc=RC.objects.get(RC_ID=user)
    return render(request,"rc/rc_scrap_collectors.html",{'user':user,'rc':rc})

def Rc_blank(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(RC_ID=user)
    return render(request,"rc/rc_blank.html",{'user':user,'rc':rc})


def Rc_profile(request):
    id=request.session.get("id")
    user=User_Master.objects.get(id=id)
    rc=RC.objects.get(RC_ID=user)
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
        rc=RC.objects.get(RC_ID=user)
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
        rc=RC.objects.get(RC_ID=user)
        return render(request,"rc/rc_update_profile.html",{'user':user,'rc':rc})
    

def Rc_orders(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(RC_ID=user)
    return render(request,"rc/rc_orders.html",{'user':user,'rc':rc})

def Rc_pricing(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(RC_ID=user)
    return render(request,"rc/rc_pricing.html",{'user':user,'rc':rc})

def Rc_product(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(RC_ID=user)
    products=Product.objects.all().filter(RC_ID=rc)
    return render(request,"rc/rc_product.html",{'user':user,'rc':rc,'products':products})



def Rc_add_product(request):
    if request.method=="POST":
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc = RC.objects.get(RC_ID=user)

        pro_name = request.POST['Pro_name']
        pro_price = request.POST['Pro_price']
        pro_desc = request.POST['Pro_desc']
        pro_img = request.FILES['Pro_img']
        seller_name=rc.Firstname+" "+rc.Lastname

        newProduct = Product.objects.create(RC_ID=rc,Seller_Name=seller_name,Product_Name=pro_name,Product_Price=pro_price,Product_Desc=pro_desc,Product_Img=pro_img,Current_orders=0)
        return HttpResponseRedirect(reverse('rc_product'))
    else:
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc=RC.objects.get(RC_ID=user)
        return render(request,"rc/rc_add_product.html",{'user':user,'rc':rc})



def RC_view_product(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc = RC.objects.get(RC_ID=user)
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
        rc = RC.objects.get(RC_ID=user)
        # return HttpResponseRedirect(reverse('RC_view_product',args={'key':product.id}))
        return HttpResponseRedirect(reverse('RC_view_product',args=[product.id]))

    else:
        id = request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc = RC.objects.get(RC_ID=user)
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
    rc=RC.objects.get(RC_ID=user)

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


def Index(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(Customer_ID=user)
    products = Product.objects.all()
    return render(request,"ecom/index.html",{'user':user,'customer':customer,'products':products})
    
def Product_detail(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(Customer_ID=user)
    product = Product.objects.get(pk=key)
    return render(request,"ecom/product_detail.html",{'user':user,'customer':customer,'product':product})

def Profile(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(Customer_ID=user)
    return render(request,"ecom/profile.html",{'user':user,'customer':customer})
    
def Logout(request):
    try:
        del request.session['id']
        del request.session['fname']
        del request.session['lname']
        return render(request,'app/login.html')
    except:
        pass

def Customer_update_profile(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        add = request.POST['add']
        contact = request.POST['contact']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        id = request.session.get("id")
        user = User_Master.objects.get(id=id)
        customer=Customer.objects.get(Customer_ID=user)
        customer.Firstname=fname
        customer.Lastname=lname
        customer.Address=add
        customer.Contact=contact
        customer.City=city
        customer.State=state
        customer.Pincode=pincode
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
        customer=Customer.objects.get(Customer_ID=user)
        return render(request,"ecom/customer_update_profile.html",{'user':user,'customer':customer})

def Change_password(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(Customer_ID=user)
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
                return render(request,"ecom/change_password.html",{'user':user,'customer':customer,'msg':msg})
            else:
                msg="New Password & Confirm Password Did Not Match!!!"
                return render(request,"ecom/change_password.html",{'user':user,'customer':customer,'msg':msg})
        else:
            msg="Old Password Is Incorect!!!"
            return render(request,"ecom/change_password.html",{'user':user,'customer':customer,'msg':msg})
    else:
        return render(request,"ecom/change_password.html",{'user':user,'customer':customer})


def add_to_cart_or_buy_now(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer = Customer.objects.get(Customer_ID=user)
    product = Product.objects.get(id=key)
    quantity = request.POST['quantity_copy']

    if 'add_to_cart' in request.POST:
        per_pro_price = product.Product_Price
        total_amt = float(quantity)*float(per_pro_price)
        new_cart_item = Cust_Cart.objects.create(Customer_ID=customer,Product_ID=product,Quantity=quantity,Per_Pro_Price=per_pro_price,Total_Amount=total_amt)
        # AHI "ITEM ADDED TO CART SUCCESSFULLY NO MESSAGE FIRE KARAVO CHE... EK MESSAGE LAI RENDER MA PASS KARVO PADE"
        # PN RENDER MA PASS KARE TYARE PRODUCT na OBJECTS.ALL() KARI MOKALJE NAI TO ERROR MARSE
        # return render(request,"ecom/index.html",{'user':user,'customer':customer,'products':product})
        return HttpResponseRedirect(reverse('product_detail',args=[product.id]))

    elif 'buy_now' in request.POST:
        print("COMING SOON.....")
        return HttpResponseRedirect(reverse('portal_sec2'))



def Cart(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(Customer_ID=user)
    cust_cart = Cust_Cart.objects.filter(Customer_ID=customer)
    return render(request,"ecom/cart.html",{'user':user,'customer':customer,'cust_cart':cust_cart})
