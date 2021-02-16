from django.db import models

# Create your models here.

class User_Master(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=300)
    Role = models.CharField(max_length=20)
    is_created = models.DateTimeField(auto_now=True,blank=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_updated = models.DateTimeField(auto_now=True,blank=False)

class Customer(models.Model):
    Customer_ID = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Profile_Pic = models.ImageField(upload_to='Profile_Pics',default="")

class GC(models.Model):
    GC_ID = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Shop_name = models.CharField(max_length=30,default="")
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Profile_Pic = models.ImageField(upload_to='Profile_Pics',default="")

class RC(models.Model):
    RC_ID = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Company_name = models.CharField(max_length=30,default="")
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Profile_Pic = models.ImageField(upload_to='Profile_Pics',default="")

class Product(models.Model):
    RC_ID = models.ForeignKey(RC,on_delete=models.CASCADE)
    Seller_Name= models.CharField(max_length=30,default="")
    Product_Name = models.CharField(max_length=30)
    Product_Price = models.FloatField()
    Product_Desc = models.TextField()
    Product_Img = models.ImageField(upload_to='Product_Images',default="")
    Current_orders = models.IntegerField(default=0)

class Cust_Cart(models.Model):
    Customer_ID = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Product_ID = models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
    Total_Amount = models.FloatField()






