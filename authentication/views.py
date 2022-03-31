
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
                    #  messages.success(request, 'Account is created Successfully!')
                     return HttpResponseRedirect('/verify/')

        else:
            form = UserCreationForm()
        return render(request,'register.html',{'form':form})
    else:
        return HttpResponseRedirect('/')




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


# def ChangePasswordd(request):
#      return render(request,'changepassword.html')



# def ChangePassword(request , token):
#     context = {}
    
    
#     try:
#         profile_obj = Profile.objects.filter(forget_password_token = token).first()
#         context = {'user_id' : profile_obj.user.id}
        
#         if request.method == 'POST':
#             new_password = request.POST.get('new_password')
#             confirm_password = request.POST.get('reconfirm_password')
#             user_id = request.POST.get('user_id')
            
#             if user_id is  None:
#                 messages.success(request, 'No user id found.')
#                 return redirect(f'/change-password/{token}/')
                
            
#             if  new_password != confirm_password:
#                 messages.success(request, 'both should  be equal.')
#                 return redirect(f'/change-password/{token}/')
                         
            
#             user_obj = User.objects.get(id = user_id)
#             user_obj.set_password(new_password)
#             user_obj.save()
#             return redirect('/login/')
            
            
            
        
        
#     except Exception as e:
#         print(e)
#     return render(request , 'change-password.html' , context)


# import uuid
# def ForgetPassword(request):
#     try:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             if not User.objects.filter(username=username).first():
#                 messages.success(request, 'Not user found with this username.')
#                 return redirect('/forget-password/')
            
#             user_obj = User.objects.get(username = username)
#             token = str(uuid.uuid4())
#             profile_obj= Profile.objects.get(user = user_obj)
#             profile_obj.forget_password_token = token
#             profile_obj.save()
#             send_forget_password_mail(user_obj.email , token)
#             messages.success(request, 'An email is sent.')
#             return redirect('/forget-password/')
                
    
    
#     except Exception as e:
#         print(e)
#     return render(request , 'forget-password.html')