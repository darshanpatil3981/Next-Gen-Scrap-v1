from django.urls import path,include
from . import views

urlpatterns = [
# Default link
     path("",views.Login_Page,name="login"),

# Direct Render
    
    #Signup Process
     path("signup_as/",views.Signup_as,name="signup_as"),
     path("enter_email/",views.Enter_email,name="enter_email"),
     path("otp_verification/",views.Otp_verification,name="otp_verification"),
     path("signup_customer/",views.Signup_customer,name="signup_customer"),


     path("signup/",views.Signup_GCRC,name="signup_GCRC"),
     
     
     
     

# Views Links (Not callable)
     path("isalreadycreated/",views.is_already_created,name="is_already_created"),
     path("verify_otp/<int:sotp>",views.verify_OTP,name="verify_OTP"),
     path("create_customer/",views.create_Customer,name="create_Customer"),
     path("validate_login/",views.Validate_login,name="validate_login"),
   
]