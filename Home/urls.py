from django.urls import path 
from .import views 

urlpatterns = [
    path("Index",views.Index,name="Index"),
    path("",views.SignIn,name="SignIn"),
    path("SignUp/<str:link>",views.SignUp,name="SignUp"),
    path("SentRefrelLink/<int:pk>",views.SentRefrelLink,name="SentRefrelLink"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("MyTeamDirect",views.MyTeamDirect,name="MyTeamDirect"),
    path("Myteam",views.Myteam,name="Myteam"),
    path("SponserIncome",views.SponserIncome,name="SponserIncome"),
    path("Levelincome",views.Levelincome,name="Levelincome"),
    path("Rebirthincome",views.Rebirthincome,name="Rebirthincome"),
    path("Withdrawal",views.Withdrawal,name="Withdrawal"),
    path("Withrawal_sponser",views.Withrawal_sponser,name="Withrawal_sponser"),
    path("Withrawal_Level",views.Withrawal_Level,name="Withrawal_Level"),
    path("WithdrawalHistory",views.WithdrawalHistory,name="WithdrawalHistory"),
    path('Rebirth',views.Rebirth,name="Rebirth")
]
