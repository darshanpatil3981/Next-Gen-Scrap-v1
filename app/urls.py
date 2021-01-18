from django.urls import path,include
from . import views

urlpatterns = [
#    path("",views.Showhome,name="home"),
     path("",views.Login_Page,name="login"),
     path("signup/",views.Signup_RCGC,name="signup"),
     path("signup_customer/",views.Signup_customer,name="signup_customer"),
     path("otp_verification/",views.Otp_verification,name="otp_verification"),
     path("create_customer/",views.create_Customer,name="create_Customer"),
     path("verify_otp/<int:key>",views.verify_OTP,name="verify_OTP"),
     path("signup_as/",views.Signup_as,name="signup_as"),
     path("enter_email/",views.Enter_email,name="enter_email"),
]