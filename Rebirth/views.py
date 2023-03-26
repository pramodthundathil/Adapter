from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TeamMembers2,UserDetails2,UserKey, TeamOne2
from datetime import datetime
from Home.models import UserDetails, TeamOne,TeamMembers

# Create your views here.
def BirthIndex(request):
    userdetails = UserDetails2.objects.get(UserId = request.user)
    T1 = TeamOne2.objects.filter(Sponser = request.user)
    T1_S = TeamOne2.objects.get(team = userdetails)
    userdetails_sponser = UserDetails2.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers2.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails2.objects.get(UserId = member.member)
        teammembers.append(m)
    context = {
        "userdetails":userdetails,
        "total":userdetails.Sponser_income + userdetails.Level_income + userdetails.ReBirth_Income,
        "T1":T1,
        'T1_count':T1.count(),
        "T1_S":userdetails_sponser,
        "teammembers":teammembers,
        "teammembers_count":len(teammembers)
    }
    return render(request,'rebirth/index.html',context)



def Rebirth(request):
    userdata = UserDetails.objects.get(UserId = request.user)
    team = TeamMembers.objects.filter(sponser = userdata)
    
    if len(team) < 20:
        messages.info(request,"You dont have 20 Team members please achive the team stregth")
        return redirect("Index")
    
    teamone =  TeamOne.objects.filter(Sponser = request.user)
    if len(teamone) < 2:
        messages.info(request,"You dont have 20 Team members please achive the team stregth")
        return redirect("Index")
    if userdata.ReBirth_Income < 50:
        messages.info(request,"You dont have Enough money")
        return redirect("Index")
    else:
        rebirthcou = 2
        if UserDetails2.objects.filter(UserId = request.user).exists():
            userdata2 = UserDetails2.objects.filter(Userid = request.user)[-1]
            rebirthcou = int(userdata2.RebirthCount) + 1
        userkey = UserKey.objects.create(UserId = request.user,User_Key = "A7{}{}{}".format(datetime.now().day,request.user.id,rebirthcou))
        userkey.save()
        details = UserDetails2.objects.create(UserId = request.user,User_Key= userkey,Hierachi_Level = 1,Sponser_income = 0,Level_income = 0,My_income = 0,ReBirth_Income = 0,RebirthCount = "2")
        details.save()
        userdata.ReBirth_Income = userdata.ReBirth_Income - 50
        userdata.save()
        userdetails = UserDetails.objects.get(UserId = request.user)
        T1 = TeamOne2.objects.create(Sponser = request.user, team = details )
        T1.save()
            
        TM = TeamMembers2.objects.create(sponser = details ,member = request.user )
        TM.save()
        messages.info(request,"Rebirth Happned")
        return redirect("Index")
        # team = TeamMembers.objects.filter(sponser = userdata)
        
def ReberthMemberadd(request, link,user):
    key = UserKey.objects.get(User_Key = link)
    details = UserDetails2.objects.get(User_key = key)
    T1 = TeamOne2.objects.create(Sponser = details.UserId, team = details )
    T1.save()
    TM = TeamMembers2.objects.create(sponser = details,member = user )
    TM.save()
    if TeamMembers2.objects.filter(member = details.UserId ).exists():
        teammember = TeamMembers2.objects.filter(member = details.UserId)
        for i in teammember:
            TM2 = TeamMembers2.objects.create(sponser = i.sponser,member = user )
            TM2.save()
    teams = TeamMembers2.objects.filter(member = user)
                
    for valu in teams:
            
        v = UserDetails2.objects.get(id = valu.sponser.id)
        v.Level_income = v.Level_income + 2.5
        v.ReBirth_Income = v.ReBirth_Income + 2.5
        v.save()
                
    messages.info(request,"User Created")
    return redirect('SignIn')
    
        
        
