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
     path("rc_change_password/",views.Rc_change_password,name="rc_change_password"),
     path("RC_view_product/<int:key>",views.RC_view_product,name="RC_view_product"),
     path("RC_edit_product/<int:key>",views.RC_edit_product,name="RC_edit_product"),
     path("RC_delete_product/<int:key>",views.RC_delete_product,name="RC_delete_product"),
     path("subscription_detail/",views.Subscription_detail,name="subscription_detail"),
     path("Invoice_Subscription/",views.Invoice_Subscription,name="invoice_subscription"),
     path("invoice_sub_pdf/<int:key>",views.Invoice_Sub_Pdf,name="invoice_sub_pdf"),
    

     #E-com
     path("index/",views.Index,name="index"),
     path("profile/",views.Profile,name="profile"),
     path("product_detail/<int:key>",views.Product_detail,name="product_detail"),
     path("logout",views.Logout,name="logout"),
     path("customer_update_profile/",views.Customer_update_profile,name="customer_update_profile"),
     path("change_password/",views.Change_password,name="change_password"),
     path("cart/",views.Cart,name="cart"),
     path("customer_orders/",views.Customer_orders,name="customer_orders"),
     path("customer_orders_detail/<int:key>",views.Customer_orders_detail,name="customer_orders_detail"),
     path("add_cart_buy/<int:key>",views.add_to_cart_or_buy_now,name="cart_buy"),
     path("edit_order/<int:key>",views.edit_order,name="edit_order"),
     path("remove_cart_item/<int:key>",views.remove_cart_item,name="remove_cart_item"),
     path("checkout/",views.Checkout,name="checkout"),
     path("shipping_detail/",views.Shipping_detail,name="shipping_detail"),
     path("invoice/",views.Invoice,name="invoice"),
     path("temp/",views.temp,name="temp"),
     path("view_Invoice/<int:key>",views.View_Invoice,name="view_Invoice"),
     path("invoice_pdf/<int:key>",views.Invoice_pdf,name="invoice_pdf"),
     

     
     
     

# Views Links (Not callable)
     path("isalreadycreated/",views.is_already_created,name="is_already_created"),
     path("verify_otp/",views.verify_OTP,name="verify_OTP"),
     path("create_customer/",views.create_Customer,name="create_Customer"),
     path("validate_login/",views.Validate_login,name="validate_login"),
     path("create_gc_rc/",views.create_gc_rc,name="create_gc_rc"),
     path("verify_OTP_forgotpw/",views.Verify_OTP_forgotpw,name="verify_OTP_forgotpw"),
     path("reset_password/",views.Reset_password,name="reset_password"),
   
]