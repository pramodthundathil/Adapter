from django.shortcuts import render, redirect, HttpResponse
from .forms import UserAddForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserDetails, TeamOne, TeamMembers,Withdrawals
from datetime import datetime
from Rebirth.models import UserDetails2,UserKey,TeamOne2,TeamMembers2


from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

def Index(request):
    rebirhdata = None
    if UserDetails2.objects.filter(UserId = request.user).exists():
        rebirhdata  = UserDetails2.objects.filter(UserId = request.user)
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
        teammembers.append(m)
    context = {
        "userdetails":userdetails,
        "total":userdetails.Sponser_income + userdetails.Level_income + userdetails.ReBirth_Income,
        "T1":T1,
        'T1_count':T1.count(),
        "T1_S":userdetails_sponser,
        "teammembers":teammembers,
        "teammembers_count":len(teammembers),
        "rebirhdata":rebirhdata
    }
    return render(request,'index.html',context)

def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or password incorrect")
            return redirect('SignIn')
        
    return render(request,'login.html')

def SignUp(request,link):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        # image = request.FILES['img']
        if form.is_valid():
            user = form.save()
            user.save()
            
            
            
            details = UserDetails.objects.create(UserId = user,User_Key = "A7{}{}".format(datetime.now().day,user.id),Hierachi_Level = 1,Sponser_income = 0,Level_income = 0,My_income = 0,ReBirth_Income = 0,RebirthCount = 0)
            details.save()
            try:
                userdetails = UserDetails.objects.get(User_Key = link)
            except:
                userkey = UserKey.objects.get(User_Key = link)
                userdetails = UserDetails2.objects.get(User_Key = userkey)
                # userdetails = UserDetails.objects.get(User_Key = link)
                
                
            # rebirth = UserDetails2.objects.all()
            # for rb in rebirth:
            #     if rb.User_Key.User_Key == link:
            #         userkey = rb.User_Key
            #         userdetails = UserDetails2.objects.get(User_Key = userkey)

            
                
            
            userdetails.Sponser_income = userdetails.Sponser_income+15
            
            if userdetails.Hierachi_Level >=3:
                userdetails.Level_income = userdetails.Level_income + 2.5
                userdetails.ReBirth_Income = userdetails.ReBirth_Income + 2.5
            userdetails.Hierachi_Level = userdetails.Hierachi_Level+1
            userdetails.save()
            
            try:
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
            except:
                pass
            try:
                T1 = TeamOne.objects.create(Sponser = userdetails.UserId, team = details )
                T1.save()
            
                TM = TeamMembers.objects.create(sponser = userdetails,member = user )
                TM.save()
            
                if TeamMembers.objects.filter(member = userdetails.UserId ).exists():
                    teammember = TeamMembers.objects.filter(member = userdetails.UserId)
                    for i in teammember:
                        TM2 = TeamMembers.objects.create(sponser = i.sponser,member = user )
                        TM2.save()
                    
                teams = TeamMembers.objects.filter(member = user)
                
                for valu in teams:
                    if valu.sponser == userdetails:
                        continue
                    v = UserDetails.objects.get(id = valu.sponser.id)
                    v.Level_income = v.Level_income + 2.5
                    v.ReBirth_Income = v.ReBirth_Income + 2.5
                    v.save()
            except:
                pass
                
            messages.info(request,"User Created")
            return redirect('SignIn')
    context  = {
        "form":form
    }
    return render(request,'register.html',context)


def SentRefrelLink(request,pk):
    try:
        userdetails = UserDetails2.objects.get(id=pk)
        activationkey = userdetails.User_Key.User_Key
    except:
        userdetails = UserDetails.objects.get(id=pk)
        activationkey = userdetails.User_Key
        
    email = request.POST['email']
    current_site = get_current_site(request)
    mail_subject = 'Join Adaper 7 Referal Link'
    path = "SignUp"
    message = render_to_string('emailbody.html', {'user': request.user,
                                                                     'domain': current_site.domain,
                                                                     'path':path,
                                                                     'token':activationkey,})

    email = EmailMessage(mail_subject, message, to=[email])
    email.send(fail_silently=True)
                
    return redirect('Index')



def SignOut(request):
    logout(request)
    return redirect("SignIn")




# Team-----------------------------------------------------------------

def MyTeamDirect(request):
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
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
    
    return render(request,"team_direct.html",context)


def Myteam(request):
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
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
    return render(request,'team.html',context)


def SponserIncome(request):
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
        teammembers.append(m)
    context = {
        "userdetails":userdetails,
        "total":userdetails.Sponser_income + userdetails.Level_income + userdetails.ReBirth_Income,
        "T1":T1,
        'T1_count':T1.count(),
        "T1_S":userdetails_sponser,
        "teammembers":teammembers,
    }
    return render(request,'sponserincome.html',context)

def Levelincome(request):
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
        teammembers.append(m)
    context = {
        "userdetails":userdetails,
        "total":userdetails.Sponser_income + userdetails.Level_income + userdetails.ReBirth_Income,
        "T1":T1,
        'T1_count':T1.count(),
        "T1_S":userdetails_sponser,
        "teammembers":teammembers,
    }
    return render(request,'levelincome.html',context)

def Rebirthincome(request):
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
        teammembers.append(m)
    context = {
        "userdetails":userdetails,
        "total":userdetails.Sponser_income + userdetails.Level_income + userdetails.ReBirth_Income,
        "T1":T1,
        'T1_count':T1.count(),
        "T1_S":userdetails_sponser,
        "teammembers":teammembers,
    }
    
    return render(request,'rebirthincome.html',context)

def Withdrawal(request):
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
        teammembers.append(m)
    context = {
        "userdetails":userdetails,
        "total":userdetails.Sponser_income + userdetails.Level_income + userdetails.ReBirth_Income,
        "T1":T1,
        'T1_count':T1.count(),
        "T1_S":userdetails_sponser,
        "teammembers":teammembers,
    }
    return render(request,'withdrawals.html',context)



# withdrowal----------------------------------

def Withrawal_sponser(request):
    if request.method == "POST":
        amount = request.POST['amount']
        userd = UserDetails.objects.get(UserId = request.user)
        income = userd.Sponser_income
        if income < float(amount):
            messages.info(request,"You Have Insufficient Fund")
            return redirect("Withdrawal")
        else:
            userd.Sponser_income = userd.Sponser_income - float(amount)
            userd.save()
            wd = Withdrawals.objects.create(user = request.user,IncomeType = "Sponserincome",Amount = amount)
            wd.save()
            messages.info(request,"Withdrawel Done")
            return redirect("Withdrawal")
            
    
def Withrawal_Level(request):
    if request.method == "POST":
        amount = request.POST['amount']
        userd = UserDetails.objects.get(UserId = request.user)
        income = userd.Level_income
        if income < float(amount):
            messages.info(request,"You Have Insufficient Fund")
            return redirect("Withdrawal")
        else:
            userd.Level_income = userd.Level_income - float(amount)
            userd.save()
            wd = Withdrawals.objects.create(user = request.user,IncomeType = "levelincome",Amount = amount)
            wd.save()
            messages.info(request,"Withdrawel Done")
            return redirect("Withdrawal")
        
def WithdrawalHistory(request):
    history = Withdrawals.objects.filter(user = request.user)
    userdetails = UserDetails.objects.get(UserId = request.user)
    T1 = TeamOne.objects.filter(Sponser = request.user)
    T1_S = TeamOne.objects.get(team = userdetails)
    userdetails_sponser = UserDetails.objects.get(UserId = T1_S.Sponser)
    team = TeamMembers.objects.filter(sponser = userdetails)
    teammembers = []
    for member in team:
        m = UserDetails.objects.get(UserId = member.member)
        teammembers.append(m)
    context = {
        "userdetails":userdetails,
        "total":userdetails.Sponser_income + userdetails.Level_income + userdetails.ReBirth_Income,
        "T1":T1,
        'T1_count':T1.count(),
        "T1_S":userdetails_sponser,
        "teammembers":teammembers,
        "history":history
    }
    return render(request,'withdrawalhistory.html',context)


# ReBirth ---------------------------------------------------

        
            
    