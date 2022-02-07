
from django.conf import settings
from .forms import UserCreationForm,LoginForm,VerifyForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .models import PreRegistration
from django.contrib.auth.models  import auth,User
from django.shortcuts import render
import random
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.mail import send_mail

#Create your views here.

def creatingOTP():
    otp = ""
    for i in range(5):
        otp+= f'{random.randint(0,9)}'
    return otp

def sendEmail(email,first_name,last_name):
    otp = creatingOTP()
    email_message = f"""
Dear {first_name} {last_name},
******* This is an automated email. Please do not reply to this email.******* 

Your One Time Password (OTP ) is {otp}.

If you have any queries, Please contact us at,
Aausadhi Pasal,
Contact 977-01-1234565

Thanks & regards
Aausadhi Pasal Limited
Lazimpat,Kathmandu, Nepal"""

    send_mail(
    'One Time Password',
    email_message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )
    return otp




def SignUp_function(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            email = request.POST.get('email')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            username=request.POST.get('username')

            if form.is_valid():
                if User.objects.filter(email=email).exists():
                    messages.info(request,'Email already taken')
                    return redirect('/reg')
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username already taken')
                    return redirect('/reg')
                else:
                     email=form.cleaned_data['email']
                     otp = sendEmail(email,first_name,last_name)
                     dt = PreRegistration(first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username= form.cleaned_data['username'],email=email,otp=otp,password1 = form.cleaned_data['password1'],password2 = form.cleaned_data['password2'])
                     dt.save()
                     messages.success(request, 'Account is created Successfully!')
                     return HttpResponseRedirect('/verify/')

        else:
            form = UserCreationForm()
        return render(request,'register.html',{'form':form})
    else:
        return HttpResponseRedirect('/')





    # if request.method == 'POST':
    #     first_name = request.POST['first_name']
    #     last_name = request.POST['last_name']
    #     username = request.POST['username']
    #     password1 = request.POST['password1']
    #     password2 = request.POST['password2']
    #     email = request.POST['email']

    #     if password1==password2:
    #         if User.objects.filter(username=username).exists():
    #             messages.info(request,'Username Taken')
    #             return redirect('reg')
    #         elif User.objects.filter(email=email).exists():
    #             messages.info(request,'Email Taken')
    #             return redirect('reg')
    #         else:   
    #             user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
    #             user.save();
    #             print('user created')
    #             return redirect('login')

    #     else:
    #         messages.info(request,'password not matching..')    
    #         return redirect('reg')
    #         return redirect('/')
        
    # else:
    #     return render(request,'register.html')



def Login_function(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)


    
    # if not request.user.is_authenticated:
    #     if request.method == 'POST':
    #         form = LoginForm(request = request,data = request.POST)
    #         if form.is_valid():
    #             username = form.cleaned_data['username']
    #             pas = form.cleaned_data['password']
    #             usr = authenticate(username= username,password=pas)
    #             login(request,usr)
    #             return HttpResponseRedirect('/')
    #     else:
    #         form = LoginForm()
    #     return render(request,'login.html',{'form':form})
    # else:
    #     return HttpResponseRedirect('/login/')
       

def verifyUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                data = PreRegistration.objects.filter(otp = otp)
                if data:
                    username = ''
                    first_name = ''
                    last_name = ''
                    email = ''
                    password1 = ''
                    for i in data:
                        print(i.username)
                        username = i.username
                        first_name = i.first_name
                        last_name = i.last_name
                        email = i.email
                        password1 = i.password1

                    user = User.objects.create_user(username, email, password1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    data.delete()
                    messages.success(request,'Account is created successfully!')
                    return HttpResponseRedirect('/login')   
                else:
                    messages.success(request,'Entered OTO is wrong')
                    return HttpResponseRedirect('/verify/')
        else:            
            form = VerifyForm()
        return render(request,'verify.html',{'form':form})
    else:
        return HttpResponseRedirect('/login')


def ChangePassword(request):
     return render(request,'changepassword.html')
