from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    User_Key = models.CharField(max_length=255)
    User_Image = models.FileField(upload_to="profile_pic",null=True,blank=True)
    Hierachi_Level = models.IntegerField()
    Sponser_income = models.FloatField(null=True)
    Level_income = models.FloatField(null=True)
    My_income = models.FloatField(null=True)
    ReBirth_Income = models.FloatField(null=True)
    RebirthCount = models.IntegerField()
    

   
class TeamOne(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)

class TeamMembers(models.Model):
    sponser = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    member = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Withdrawals(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    IncomeType = models.CharField(max_length=255)
    Amount = models.CharField(max_length=20)
    
    
