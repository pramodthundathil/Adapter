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
    
class TeamOne(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)

class TeamTwo(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)

class TeamThree(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)
    

class TeamFour(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)
    

class TeamFive(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)


class TeamSix(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)


class TeamSeven(models.Model):
    Sponser = models.ForeignKey(User,models.SET_NULL,null=True)
    team = models.ForeignKey(UserDetails,models.CASCADE)
    
class ChainLevel(models.Model):
    Sponser = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    Team1 = models.ForeignKey(TeamOne,models.SET_NULL,null=True,blank=True)
    Team2 = models.ForeignKey(TeamTwo,models.SET_NULL,null=True,blank=True)
    Team3 = models.ForeignKey(TeamThree,models.SET_NULL,null=True,blank=True)
    Team4 = models.ForeignKey(TeamFour,models.SET_NULL,null=True,blank=True)
    Team5 = models.ForeignKey(TeamFive,models.SET_NULL,null=True,blank=True)
    Team6 = models.ForeignKey(TeamSix,models.SET_NULL,null=True,blank=True)
    Team7 = models.ForeignKey(TeamSeven,models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return str(self.Sponser.first_name + " " + self.Sponser.username)
    
class TeamMembers(models.Model):
    sponser = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    member = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Withdrawals(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    IncomeType = models.CharField(max_length=255)
    Amount = models.CharField(max_length=20)
    
    
