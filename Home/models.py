from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    User_Key = models.CharField(max_length=255)
    User_Image = models.FileField(upload_to="profile_pic")
    Hierachi_Level = models.IntegerField()
    Sponser_income = models.FloatField(null=True)
    Level_income = models.FloatField(null=True)
    My_income = models.FloatField(null=True)
    ReBirth_Income = models.FloatField(null=True)
    
    
