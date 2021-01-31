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

     #RC Dashboard
     path("rc_blank/",views.Rc_blank,name="rc_blank"),
     path("rc_scrap_collectors/",views.Rc_scrap_collectors,name="rc_scrap_collectors"),
     path("rc_profile/",views.Rc_profile,name="rc_profile"),
     path("rc_update_profile/",views.Rc_update_profile,name="rc_update_profile"),
     path("rc_orders/",views.Rc_orders,name="rc_orders"),
     path("rc_pricing/",views.Rc_pricing,name="rc_pricing"),
     path("rc_product/",views.Rc_product,name="rc_product"),
     path("rc_add_product/",views.Rc_add_product,name="rc_add_product"),
     path("RC_view_product/<int:key>",views.RC_view_product,name="RC_view_product"),
     path("RC_edit_product/<int:key>",views.RC_edit_product,name="RC_edit_product"),
     
     

# Views Links (Not callable)
     path("isalreadycreated/",views.is_already_created,name="is_already_created"),
     path("verify_otp/",views.verify_OTP,name="verify_OTP"),
     path("create_customer/",views.create_Customer,name="create_Customer"),
     path("validate_login/",views.Validate_login,name="validate_login"),
     path("create_gc_rc/",views.create_gc_rc,name="create_gc_rc"),
     path("verify_OTP_forgotpw/",views.Verify_OTP_forgotpw,name="verify_OTP_forgotpw"),
     path("reset_password/",views.Reset_password,name="reset_password"),
   
]