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
     path("forgot_password/",views.Forgot_password,name="forgot_password"),


     path("signup/",views.Signup_GCRC,name="signup_GCRC"),
     
     path("tempDarsh/",views.temp,name="temp"),
     
     

# Views Links (Not callable)
     path("isalreadycreated/",views.is_already_created,name="is_already_created"),
     path("verify_otp/",views.verify_OTP,name="verify_OTP"),
     path("create_customer/",views.create_Customer,name="create_Customer"),
     path("validate_login/",views.Validate_login,name="validate_login"),
     path("create_gc_rc/",views.create_gc_rc,name="create_gc_rc"),
     path("verify_OTP_forgotpw/",views.Verify_OTP_forgotpw,name="verify_OTP_forgotpw"),
     path("reset_password/",views.Reset_password,name="reset_password"),
   
]