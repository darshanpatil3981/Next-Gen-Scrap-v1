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
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def Rc_Purchase_Scrap(request):
    cat = Scrap_Categories.objects.all()
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)

    paginator = Paginator(cat,8)
    page = request.GET.get('page')
    paged_cat = paginator.get_page(page)

    return render(request,"rc/rc_purchase_scrap.html",{'cat':paged_cat,'rc':rc})


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
    
    paginator = Paginator(order_product,4)
    page = request.GET.get('page')
    paged_order_product = paginator.get_page(page)
    return render(request,"rc/rc_orders.html",{'user':user,'rc':rc,'order_product':paged_order_product})

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
    products=Product.objects.all().filter(RC=rc).order_by('id')

    paginator = Paginator(products,4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    return render(request,"rc/rc_product.html",{'user':user,'rc':rc,'products':paged_products})    
    # return render(request,"rc/rc_product.html",{'user':user,'rc':rc,'products':products})

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




def Select_Sc(request,key):
    cat = Scrap_Categories.objects.get(id=key)
    name=cat.Name
    stock = Scrap_Stock.objects.filter(Name=name,In_Stock=True)
    return render(request,"rc/select_sc.html",{'stock':stock})

def Enter_RC_Scrap_Request_Detail(request,key):
    stock_id = key
    return render(request,"rc/enter_scrap_request_detail.html",{'stock_id':stock_id})

def RC_Confirm_Scrap_Request(request):
    if request.method=="POST":
        datetime = request.POST['datetime']
        quantity = request.POST['quantity']
        stock_id = request.POST['stock_id']

        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        rc=RC.objects.get(User_Master=user)
        stock = Scrap_Stock.objects.get(id=stock_id)
        sc_id = stock.SC.id
        sc = SC.objects.get(id=sc_id)
        print(sc)
        new_rc_scrap_request = RC_Scrap_Request.objects.create(
            RC = rc,
            SC = sc,
            Scrap_Stock = stock,
            Quantity = quantity,
            Datetime_of_request = datetime,
        )
        email = user.Email
        email_Subject = "Your Scrap request Has been Sent"
        sendmail_scrap_request(email_Subject,'scrap_request_email',email,{'req':new_rc_scrap_request}) 

    return HttpResponseRedirect(reverse('rc_scrap_request_detail',args=[new_rc_scrap_request.id]))
    
    # return redirect('rc_scrap_requests')
        
    


def RC_Scrap_Requests(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    rc=RC.objects.get(User_Master=user)
    req = RC_Scrap_Request.objects.filter(RC=rc)
    paginator = Paginator(req,6)
    page = request.GET.get('page')
    paged_req = paginator.get_page(page)
    return render(request,"rc/rc_scrap_requests.html",{'req':paged_req,'rc':rc})

def RC_Scrap_Request_Detail(request,key):
    req = RC_Scrap_Request.objects.get(id=key)
    print(req)
    return render(request,"rc/rc_scrap_request_detail.html",{'req':req})
