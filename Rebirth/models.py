from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserKey(models.Model):
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    User_Key = models.CharField(max_length=255)

class UserDetails2(models.Model):
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    User_Key = models.ForeignKey(UserKey,on_delete=models.CASCADE)
    # User_Image = models.FileField(upload_to="profile_pic",null=True,blank=True)
    Hierachi_Level = models.IntegerField()
    Sponser_income = models.FloatField(null=True)
    Level_income = models.FloatField(null=True)
    My_income = models.FloatField(null=True)
    ReBirth_Income = models.FloatField(null=True)
    RebirthCount = models.IntegerField()
    
class TeamOne2(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails2,models.CASCADE)
    
class TeamMembers2(models.Model):
    sponser = models.ForeignKey(UserDetails2,on_delete=models.CASCADE)
    member = models.ForeignKey(User,on_delete=models.CASCADE)
    


