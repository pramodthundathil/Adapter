from django.urls import path 
from .import views 

urlpatterns = [
    path("Index",views.Index,name="Index"),
    path("",views.SignIn,name="SignIn"),
    path("SignUp/<str:link>",views.SignUp,name="SignUp"),
    path("SentRefrelLink/<int:pk>",views.SentRefrelLink,name="SentRefrelLink")
]
