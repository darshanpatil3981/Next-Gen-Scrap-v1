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


def Index(request):
    products = Product.objects.all()
    if 'term' in request.GET:
        #qs = Product.objects.filter(Product_Name__istartswith=request.GET.get('term'))
        qs = Product.objects.filter(Product_Name__icontains=request.GET.get('term'))
        suggested_names = list()
        for item in qs:
            suggested_names.append(item.Product_Name)
        print("================================================================")
        print(suggested_names)
        return JsonResponse(suggested_names,safe=False)
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
    pdf = render_to_pdf('ecom/invoice_pdf.html',data)
    return HttpResponse(pdf, content_type='application/pdf')
    
def temp(request):
    return render(request,"temp.html")


def Add_coomment_ecom(request,key):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    product = Product.objects.get(id=key)

    cmt_text = request.POST['cmt_msg']
    cmt_date = datetime.now().date()
    
    cmt_obj = Ecom_comments.objects.create(Product=product,Customer=customer,Comment_text=cmt_text,Comment_time=cmt_date)
   
    return HttpResponseRedirect(reverse('product_detail',args=[product.id]))


def Search(request):
    result = request.POST['result']
    products = Product.objects.filter(Product_Name__icontains = result)
    return render(request,"ecom/search_result.html",{'products':products})

def Select_Area(request):
    areas = Areas.objects.all()
    return render(request,"ecom/select_area.html",{'areas':areas})

def Select_Scrap_Collector(request):
    area1 = request.POST['area']
    sc = SC.objects.filter(Area=area1)
    return render(request,"ecom/select_scrap_collector.html",{'sc':sc})
    
def Scrap_Request_Detail(request,key):
    return render(request,"ecom/scrap_request_detail.html",{'id':key})
    
def Confirm_Scrap_Request(request):
    if request.method=="POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        add = request.POST['add']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        datetime = request.POST['datetime']
        sc_id = request.POST['sc_id']

        id = request.session.get("id")
        user = User_Master.objects.get(id=id)
        customer=Customer.objects.get(User_Master=user)
        sc = SC.objects.get(id=sc_id)

        new_customer_scrap_request = Customer_Scrap_Request.objects.create(
            Customer = customer,
            SC = sc,
            Name = name,
            Phone = phone,
            Email = email,
            Address = add,
            Pincode = pincode,
            City = city,
            State = state,
            Datetime_Of_Pickup = datetime,

        )
        return HttpResponseRedirect(reverse('my_scrap_request_detail',args=[new_customer_scrap_request.id]))

        # return redirect('my_scrap_requests')
    return render(request,"ecom/index.html")
    
def My_Scrap_Requests(request):
    id = request.session.get("id")
    user = User_Master.objects.get(id=id)
    customer=Customer.objects.get(User_Master=user)
    req = Customer_Scrap_Request.objects.filter(Customer=customer)
    return render(request,"ecom/my_scrap_requests.html",{'req':req})

def My_Scrap_Request_Detail(request,key):
    req = Customer_Scrap_Request.objects.get(id=key)
    return render(request,"ecom/my_scrap_request_detail.html",{'req':req})