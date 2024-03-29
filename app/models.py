from django.db import models
from django.utils import timezone

# Create your models here.

class User_Master(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=300)
    Role = models.CharField(max_length=20)
    is_created = models.DateTimeField(auto_now=True,blank=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    Verify_Request = models.BooleanField(default=False)


class Customer(models.Model):
    User_Master = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Profile_Pic = models.ImageField(upload_to='Profile_Pics',default="user.png")

class SC(models.Model):
    User_Master = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Shop_name = models.CharField(max_length=30,default="")
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    Area = models.CharField(max_length=30,null=True, blank=True)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Is_Subscription_Active = models.BooleanField(default=False)
    Profile_Pic = models.ImageField(upload_to='Profile_Pics',default="user.png")
    Document_Type = models.CharField(max_length = 30,null=True)
    Document_File = models.FileField(upload_to ='User_Documents/',null=True)

class RC(models.Model):
    User_Master = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Company_name = models.CharField(max_length=30,default="")
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Is_Subscription_Active = models.BooleanField(default=False)
    Profile_Pic = models.ImageField(upload_to='Profile_Pics',default="user.png")
    Document_Type = models.CharField(max_length = 30,null=True)
    Document_File = models.FileField(upload_to ='User_Documents/',null=True)

class Product(models.Model):
    RC = models.ForeignKey(RC,on_delete=models.CASCADE)
    Seller_Name= models.CharField(max_length=30,default="")
    Product_Name = models.CharField(max_length=30)
    Product_Price = models.FloatField()
    Product_Desc = models.TextField()
    Product_Img = models.ImageField(upload_to='Product_Images',default="")
    Current_orders = models.IntegerField(default=0)

class Cust_Cart(models.Model):
    Customer= models.ForeignKey(Customer,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
    Total_Amount = models.IntegerField(default=0)

class Order(models.Model):
    Order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Total_Amount = models.FloatField(default=0)
    Sub_Total_Amount = models.FloatField(default=0)
    Payment_status = models.CharField(max_length=20, null=True, blank=True)
    Status = models.CharField(max_length=20, null=True, blank=True)
    Datetime_of_payment = models.DateField(null=True) 
    Estimate_Delivery_Date = models.DateField(null=True) 
    Invoice_No = models.BigIntegerField(default=0)
    Razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    Razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

class Product_Order(models.Model):
    Order = models.ForeignKey(Order, on_delete = models.CASCADE)
    RC_ID = models.CharField(max_length=20, null=True, blank=True)
    Customer = models.CharField(max_length=20,null=True, blank=True)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Cart_ID = models.CharField(max_length=20,null=True, blank=True)
    Payment_status= models.CharField(max_length=20, null=True, blank=True)
    Quantity = models.PositiveIntegerField()
    Price = models.FloatField(default=0)

class Subscription(models.Model):
    User = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Role = models.CharField(max_length=10, null=True, blank=True)
    Is_Active = models.BooleanField() 
    Subscription_Name = models.CharField(max_length=20,null=True, blank=True)
    Subscription_Amount = models.FloatField(default=0)
    Subscription_Starting_Date = models.DateField() 
    Subscription_Ending_Date = models.DateField() 
    Invoice_No = models.BigIntegerField(default=0)
    Razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    Razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)


class Ecom_comments(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Comment_text = models.CharField(max_length=500)
    Comment_time = models.DateTimeField()

class Admin(models.Model):
    User_Name = models.EmailField(max_length=50)
    Password = models.CharField(max_length=300)

class Scrap_Categories(models.Model):
    Name = models.CharField(max_length=20,null=True, blank=True)
    Price = models.FloatField()
    Image = models.ImageField(upload_to='Scrap_Images',default="default.png")

class Scrap_Stock(models.Model):
    SC = models.ForeignKey(SC,on_delete=models.CASCADE)
    Quantity = models.IntegerField(null=True)
    Name = models.CharField(max_length=20,null=True, blank=True)
    Price = models.FloatField()
    Image = models.ImageField(upload_to='Scrap_Images',default="default.png")
    In_Stock = models.BooleanField() 

class RC_Scrap_Request(models.Model):
    RC = models.ForeignKey(RC,on_delete=models.CASCADE)
    SC = models.ForeignKey(SC,on_delete=models.CASCADE)
    Scrap_Stock = models.ForeignKey(Scrap_Stock,on_delete=models.CASCADE)
    Quantity = models.IntegerField(null=True)
    Datetime_of_request = models.DateTimeField() 
    Is_Complited = models.BooleanField(default=False)

class Areas(models.Model):
    Name = models.CharField(max_length=30,null=True, blank=True)

class Customer_Scrap_Request(models.Model):
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    SC = models.ForeignKey(SC,on_delete=models.CASCADE)
    Name = models.CharField(max_length=50,null=True, blank=True)
    Phone = models.BigIntegerField()
    Email = models.EmailField()
    Address = models.CharField(max_length=200,null=True, blank=True)
    Pincode = models.IntegerField()
    City = models.CharField(max_length=20,null=True, blank=True)
    State = models.CharField(max_length=20,null=True, blank=True)
    Datetime_Of_Pickup = models.DateTimeField()
    Is_Complited = models.BooleanField(default=False)
    
class contect_Messages(models.Model):
    Name = models.CharField(max_length=50,null=True, blank=True)
    Email = models.CharField(max_length=50,null=True, blank=True)
    Subject = models.CharField(max_length=100,null=True, blank=True)
    Message = models.CharField(max_length=500,null=True, blank=True)


    







    


    















