from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.Showhome,name="home"),
     path("login/",views.Login,name="login"),
     path("signin/",views.Signin,name="signin"),
     path("signin_customer/",views.Signin_customer,name="signin_customer"),
     path("otp_verification/",views.Otp_verification,name="otp_verification"),
]