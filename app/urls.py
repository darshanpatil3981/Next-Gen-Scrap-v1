from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.Showhome,name="home"),
     path("login/",views.Login,name="login"),
     path("register/",views.Register,name="register"),
     
]