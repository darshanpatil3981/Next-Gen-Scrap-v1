from django.db import models

# Create your models here.

class User_Master(models.Model):
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Role = models.CharField(max_length=20)
    Otp = models.IntegerField()
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
    Profile_Pic = models.ImageField(default='d.jpg',upload_to='app/Profile_Pics')

class GC(models.Model):
    GC_ID = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Profile_Pic = models.ImageField(default='d.jpg',upload_to='app/Profile_Pics')

class RC(models.Model):
    RC_ID = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=30)
    Lastname = models.CharField(max_length=30)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Contact = models.BigIntegerField(default=0)
    Profile_Pic = models.ImageField(default='d.jpg',upload_to='app/Profile_Pics')