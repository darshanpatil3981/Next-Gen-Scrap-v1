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

def Invoice_Sub_Pdff(request,key):
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


def Request_Verify(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    user.Verify_Request=True
    user.save()
    if(user.Role=="RC"):
        return redirect('rc_profile')
    elif(user.Role=="SC"):
        return redirect('sc_profile')