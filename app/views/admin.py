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

def Verify_Rc_Profile(request):
    rc = RC.objects.all()
    return render(request,"ngs_admin/verify_rc_profile.html",{'rc':rc})

def Delete_Scrap_Category(request,key):
    delcat = Scrap_Categories.objects.get(id=key)
    if(delcat.Image):
       delcat.Image.delete()
    delcat.delete()
    return redirect('scrap_categories')


def Admin_view_rc_profile(request,key):
    rc=RC.objects.get(id=key)
    return render(request,"ngs_admin/admin_view_rc_profile.html",{'rc':rc})

def Change_Verify_Status(request,key):
    rc=RC.objects.get(id=key)
    user_id=rc.User_Master.id
    user = User_Master.objects.get(id=user_id)
    if(user.is_verified==True):
        user.is_verified=False
        user.Verify_Request=False
        user.save()
        return redirect('rc_profiles')
    elif(user.is_verified==False):
        user.is_verified=True
        user.Verify_Request=False
        user.save()
        return redirect('rc_profiles')
    
def Rc_Profiles(request):
    rc=RC.objects.all()
    return render(request,"ngs_admin/rc_profiles.html",{'rc':rc})
def Verified_Rc_Profiles(request):
    rc=RC.objects.all()
    return render(request,"ngs_admin/verified_rc_profiles.html",{'rc':rc})

def Sc_Profiles(request):
    sc=SC.objects.all()
    return render(request,"ngs_admin/sc_profiles.html",{'sc':sc})

def Customer_Profiles(request):
    customer = Customer.objects.all()
    return render(request,"ngs_admin/customer_profiles.html",{'customer':customer})

def Verify_Sc_Profile(request):
    sc = SC.objects.all()
    return render(request,"ngs_admin/verify_sc_profile.html",{'sc':sc})

def Admin_view_Sc_profile(request,key):
    sc=SC.objects.get(id=key)
    return render(request,"ngs_admin/admin_view_sc_profile.html",{'sc':sc})

def Change_Verify_Status_Sc(request,key):
    sc=SC.objects.get(id=key)
    user_id=sc.User_Master.id
    user = User_Master.objects.get(id=user_id)
    print(sc)
    print(user.id)
    if(user.is_verified==True):
        user.is_verified=False
        user.Verify_Request=False
        user.save()
        return redirect('sc_profiles')
    elif(user.is_verified==False):
        user.is_verified=True
        user.Verify_Request=False
        user.save()
        print(user.is_verified)
        print(user.Verify_Request)
        return redirect('sc_profiles')
    
def Verified_Sc_Profiles(request):
    sc=SC.objects.all()
    return render(request,"ngs_admin/verified_sc_profiles.html",{'sc':sc})
