from django.shortcuts import render, redirect, HttpResponse
from .forms import UserAddForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserDetails
from datetime import datetime


from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

def Index(request):
    userdetails = UserDetails.objects.get(UserId = request.user)
    context = {
        "userdetails":userdetails
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
        image = request.FILES['img']
        if form.is_valid():
            user = form.save()
            user.save()
            details = UserDetails.objects.create(UserId = user,User_Key = "A7{}{}".format(datetime.now().day,user.id),Hierachi_Level = 1,User_Image = image,Sponser_income = 0,Level_income = 0,My_income = 0,ReBirth_Income = 0)
            details.save()
            userdetails = UserDetails.objects.get(User_Key = link)
            userdetails.Sponser_income = userdetails.Sponser_income+15
            if userdetails.Hierachi_Level >=3:
                userdetails.Level_income = userdetails.Level_income + 2.5
                userdetails.ReBirth_Income = userdetails.ReBirth_Income + 2.5
            userdetails.Hierachi_Level = userdetails.Hierachi_Level+1
            userdetails.save()
            messages.info(request,"User Created")
            return redirect('SignIn')
    context  = {
        "form":form
    }
    return render(request,'register.html',context)


def SentRefrelLink(request,pk):
    userdetails = UserDetails.objects.get(id=pk)
    activationkey = userdetails.User_Key
    email = request.POST['email']
    current_site = get_current_site(request)
    mail_subject = 'Activate your E-Cart account.'
    path = "SignUp"
    message = render_to_string('emailbody.html', {'user': request.user,
                                                                     'domain': current_site.domain,
                                                                     'path':path,
                                                                     'token':activationkey,})

    email = EmailMessage(mail_subject, message, to=[email])
    email.send(fail_silently=True)
                
    return redirect('Index')
    