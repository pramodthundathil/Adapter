from django.urls import path
from .import views

urlpatterns = [
    path('Rebirth',views.Rebirth,name="Rebirth"),
    path("BirthIndex",views.BirthIndex,name="BirthIndex")
    
]
