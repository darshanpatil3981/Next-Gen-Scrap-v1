from django.urls import path,include
from . import views
from .views import login_singup
from .views import rc
from .views import sc
from .views import subscription
from .views import ecom
from .views import admin
urlpatterns = [
# Default link
     path("login/",login_singup.Login_Page,name="login"),

# Direct Render
    
    #New
    path("",login_singup.Home,name="home"),
    path("about_us/",login_singup.About_Us,name="about_us"),
    path("contact/",login_singup.Contact,name="contact"),

    #Signup Process
     
     path("signup_as/",login_singup.Signup_as,name="signup_as"),
     path("enter_email/",login_singup.Enter_email,name="enter_email"),
     path("otp_verification/",login_singup.Otp_verification,name="otp_verification"),
     path("signup_customer/",login_singup.Signup_customer,name="signup_customer"),
     path("forgot_password/",login_singup.Forgot_password,name="forgot_password"),


    path("signup/",login_singup.Signup_GCRC,name="signup_GCRC"),

     #RC Dashboard
     path("rc_blank/",rc.Rc_blank,name="rc_blank"),
     path("rc_purchase_scrap/",rc.Rc_Purchase_Scrap,name="rc_purchase_scrap"),
     path("view_sc_profile/<int:key>",rc.View_Sc_Profile,name="view_sc_profile"),
     path("rc_profile/",rc.Rc_profile,name="rc_profile"),
     path("rc_update_profile/",rc.Rc_update_profile,name="rc_update_profile"),
     path("rc_orders/",rc.Rc_orders,name="rc_orders"),
     path("rc_pricing/",rc.Rc_pricing,name="rc_pricing"),
     path("rc_product/",rc.Rc_product,name="rc_product"),
     path("rc_add_product/",rc.Rc_add_product,name="rc_add_product"),
     path("rc_change_password/",rc.Rc_change_password,name="rc_change_password"),
     path("RC_view_product/<int:key>",rc.RC_view_product,name="RC_view_product"),
     path("RC_edit_product/<int:key>",rc.RC_edit_product,name="RC_edit_product"),
     path("RC_delete_product/<int:key>",rc.RC_delete_product,name="RC_delete_product"),

     path("select_sc/<int:key>",rc.Select_Sc,name="select_sc"),
     path("rc_scrap_request_detail/<int:key>",rc.RC_Scrap_Request_Detail,name="rc_scrap_request_detail"),
     path("enter_rc_scrap_request_detail/<int:key>",rc.Enter_RC_Scrap_Request_Detail,name="enter_rc_scrap_request_detail"),
     path("rc_confirm_scrap_request/",rc.RC_Confirm_Scrap_Request,name="rc_confirm_scrap_request"),
     path("rc_scrap_requests/",rc.RC_Scrap_Requests,name="rc_scrap_requests"),


     # SC RC Subscription

     path("subscription_detail/",subscription.Subscription_detail,name="subscription_detail"),
     path("Invoice_Subscription/",subscription.Invoice_Subscription,name="invoice_subscription"),
     path("invoice_sub_pdff/<int:key>",subscription.Invoice_Sub_Pdff,name="invoice_sub_pdff"),
     path("request_verify/",subscription.Request_Verify,name="request_verify"),
     path("view_subscription/",subscription.View_subscription,name="view_subscription"),
    

     #SC Dashboard
     path("sc_update_profile/",sc.Sc_Update_Profile,name="sc_update_profile"),
     path("sc_profile/",sc.Sc_Profile,name="sc_profile"),
     path("sc_change_password/",sc.Sc_Change_Password,name="sc_change_password"),
     path("sc_pricing/",sc.Sc_Pricing,name="sc_pricing"),
     path("sc_scrap_sock/",sc.Sc_Scrap_Stock,name="sc_scrap_sock"),
     path("sc_scrap_request_customer/",sc.Sc_Scrap_Request_Customer,name="sc_scrap_request_customer"),
     path("sc_scrap_request_rc/",sc.Sc_Scrap_Request_Rc,name="sc_scrap_request_rc"),
     path("add_tock/",sc.Add_Stock,name="add_stock"),
     path("delete_stock/<int:key>",sc.Delete_stock,name="delete_stock"),
     path("update_stock/<int:key>",sc.Update_Stock,name="update_stock"),
     path("sc_scrap_request_detail/<int:key>",sc.Sc_Scrap_Request_Detail,name="sc_scrap_request_detail"),
     path("change_request_status/<int:key>",sc.Change_Request_Status,name="change_request_status"),
     path("change_request_status_rc/<int:key>",sc.Change_Request_Status_Rc,name="change_request_status_rc"),
     path("scrap_request_detail_rc/<int:key>",sc.Scrap_Request_Detail_Rc,name="scrap_request_detail_rc"),

    

     #E-com
     path("index/",ecom.Index,name="index"),
     path("profile/",ecom.Profile,name="profile"),
     path("product_detail/<int:key>",ecom.Product_detail,name="product_detail"),
     path("logout",ecom.Logout,name="logout"),
     path("customer_update_profile/",ecom.Customer_update_profile,name="customer_update_profile"),
     path("change_password/",ecom.Change_password,name="change_password"),
     path("cart/",ecom.Cart,name="cart"),
     path("customer_orders/",ecom.Customer_orders,name="customer_orders"),
     path("customer_orders_detail/<int:key>",ecom.Customer_orders_detail,name="customer_orders_detail"),
     path("add_cart_buy/<int:key>",ecom.add_to_cart_or_buy_now,name="cart_buy"),
     path("edit_order/<int:key>",ecom.edit_order,name="edit_order"),
     path("remove_cart_item/<int:key>",ecom.remove_cart_item,name="remove_cart_item"),
     path("checkout/",ecom.Checkout,name="checkout"),
     path("shipping_detail/",ecom.Shipping_detail,name="shipping_detail"),
     path("invoice/",ecom.Invoice,name="invoice"),
     path("temp/",ecom.temp,name="temp"),
     path("search/",ecom.Search,name="search"),
     path("view_Invoice/<int:key>",ecom.View_Invoice,name="view_Invoice"),
     path("invoice_pdf/<int:key>",ecom.Invoice_pdf,name="invoice_pdf"),
     path("add_coomment/<int:key>",ecom.Add_coomment_ecom,name="add_coomment_ecom"),
     path("select_area/",ecom.Select_Area,name="select_area"),
     path("select_scrap_collector/",ecom.Select_Scrap_Collector,name="select_scrap_collector"),
     path("scrap_request_detail/<int:key>",ecom.Scrap_Request_Detail,name="scrap_request_detail"),
     path("my_scrap_request_detail/<int:key>",ecom.My_Scrap_Request_Detail,name="my_scrap_request_detail"),
     path("confirm_scrap_request/",ecom.Confirm_Scrap_Request,name="confirm_scrap_request"),
     path("my_scrap_requests/",ecom.My_Scrap_Requests,name="my_scrap_requests"),
     path("scrap_prices/",ecom.Scrap_Prices,name="scrap_prices"),


     
     

     
     

# Views Links (Not callable)
     path("isalreadycreated/",login_singup.is_already_created,name="is_already_created"),
     path("verify_otp/",login_singup.verify_OTP,name="verify_OTP"),
     path("create_customer/",login_singup.create_Customer,name="create_Customer"),
     path("validate_login/",login_singup.Validate_login,name="validate_login"),
     path("create_gc_rc/",login_singup.create_gc_rc,name="create_gc_rc"),
     path("verify_OTP_forgotpw/",login_singup.Verify_OTP_forgotpw,name="verify_OTP_forgotpw"),
     path("reset_password/",login_singup.Reset_password,name="reset_password"),
   

   #Admin
     path("ngs_admin/",admin.Ngs_Admin,name="ngs_admin"),
     path("scrap_categories/",admin.Scrap_Categories1,name="scrap_categories"),
     path("add_scrap_categories/",admin.Add_Scrap_Categories,name="add_scrap_categories"),
     path("edit_scrap_category/<int:key>",admin.Edit_Scrap_Category,name="edit_scrap_category"),
     path("delete_scrap_category/<int:key>",admin.Delete_Scrap_Category,name="delete_scrap_category"),
     path("verify_rc_profile/",admin.Verify_Rc_Profile,name="verify_rc_profile"),
     path("admin_view_rc_profile/<int:key>",admin.Admin_view_rc_profile,name="admin_view_rc_profile"),
     path("change_verify_status/<int:key>",admin.Change_Verify_Status,name="change_verify_status"),
     path("sc_profiles/",admin.Sc_Profiles,name="sc_profiles"),
     path("rc_profiles/",admin.Rc_Profiles,name="rc_profiles"),
     path("customer_profiles/",admin.Customer_Profiles,name="customer_profiles"),
     path("verified_rc_profiles/",admin.Verified_Rc_Profiles,name="verified_rc_profiles"),
     path("verify_sc_profile/",admin.Verify_Sc_Profile,name="verify_sc_profile"),
     path("admin_view_sc_profile/<int:key>",admin.Admin_view_Sc_profile,name="admin_view_sc_profile"),
     path("change_verify_status_sc/<int:key>",admin.Change_Verify_Status_Sc,name="change_verify_status_sc"),
     path("verified_sc_profiles/",admin.Verified_Sc_Profiles,name="verified_sc_profiles"),
     path("areas/",admin.Areas11,name="areas"),
     path("add_area/",admin.Add_Area,name="add_area"),
     path("remove_area/<int:key>",admin.Remove_Area,name="remove_area"),








]