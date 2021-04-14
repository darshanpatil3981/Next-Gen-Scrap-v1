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

def Sc_Profile(request):
    id=request.session.get("id")
    user=User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    return render(request,"sc/sc_profile.html",{'user':user,'sc':sc})

def Sc_Update_Profile(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        add = request.POST['add']
        contact = request.POST['contact']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        area = request.POST['area']
      

        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        sc=SC.objects.get(User_Master=user)
        sc.Firstname=fname
        sc.Lastname=lname
        sc.Area = area
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
        areas = Areas.objects.all()
        return render(request,"sc/sc_update_profile.html",{'user':user,'sc':sc,'areas':areas})

def Sc_Change_Password(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
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
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)

    scrap_categories = Scrap_Categories.objects.all()
    scrap_stock = Scrap_Stock.objects.filter(SC=sc)
    return render(request,"sc/sc_scrap_sock.html",{'sc':sc,'scrap_categories':scrap_categories,'scrap_stock':scrap_stock})

def Sc_Scrap_Request_Customer(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    req = Customer_Scrap_Request.objects.filter(SC=sc)
    print('-------------')
    print(req)
    return render(request,"sc/sc_scrap_request_customer.html",{'sc':sc,'req':req})

def Sc_Scrap_Request_Detail(request,key):
    req = Customer_Scrap_Request.objects.get(id=key)
    return render(request,"sc/sc_scrap_request_detail.html",{'req':req})

def Change_Request_Status(request,key):
    req = Customer_Scrap_Request.objects.get(id=key)
    if (req.Is_Complited == True):
        req.Is_Complited = False
    elif(req.Is_Complited == False):
        req.Is_Complited = True
    req.save()
    return redirect('sc_scrap_request_customer')



def Change_Request_Status_Rc(request,key):
    req = RC_Scrap_Request.objects.get(id=key)
    if (req.Is_Complited == True):
        req.Is_Complited = False
    elif(req.Is_Complited == False):
        req.Is_Complited = True
    req.save()
    return redirect('sc_scrap_request_rc')


 



def Sc_Scrap_Request_Rc(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    print("------------------")
    print(sc)
    req = RC_Scrap_Request.objects.filter(SC=sc)
    return render(request,"sc/sc_scrap_request_rc.html",{'sc':sc,'req':req})




def Add_Stock(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    sc=SC.objects.get(User_Master=user)
    cat_name=request.POST['sname']
    q =  request.POST['quantity']
   
    cat = Scrap_Categories.objects.get(Name=cat_name)
    new_scrap = Scrap_Stock.objects.create(Name=cat.Name,Price=cat.Price,Image=cat.Image,In_Stock=True,SC=sc,Quantity=q)
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
        stock.Quantity =0
        stock.In_Stock=False
    elif(stock.In_Stock==False):
        stock.In_Stock=True
    stock.save()
    return redirect('sc_scrap_sock')

def Scrap_Request_Detail_Rc(request,key):
    req = RC_Scrap_Request.objects.get(id=key)
    return render(request,"sc/sc_scrap_request_detail_rc.html",{'req':req})

