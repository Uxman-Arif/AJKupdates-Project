from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
emailreciept = []
signinemailreciept = []

# Create your views here.
@login_required(login_url = '/signin')
def index(request):
    posting = post.objects.all()
    print('loading outside')
    if request.method == 'POST':
        print('loading inside')
        like = request.POST.get('like')
        print(like)
    context = {'posts':posting}
    return render(request, 'home.html', context)

def signup(request):  
    if request.method == 'POST':  
        username = request.POST.get('signupname')   
        email = request.POST.get('email')  
        password = request.POST.get('signuppassword')  
        
        # Create user account but don't activate it yet  
        userregister = User(username=username, email=email)  
        userregister.set_password(password.strip())  
        userregister.is_active = False  
        userregister.save()  

        # Generate OTP  
        otp_code = str(random.randint(1000, 9999))  
        print(otp_code)

        # Save OTP in the database  
        otp_record = OTP.objects.create(user=userregister, otp_code=otp_code)  

        # Send the OTP via email  
        subject = 'Email Verification'  
        message = f'Your OTP is {otp_code}'  
        from_email = settings.EMAIL_HOST_USER  
        recipient_list = [email]  
        send_mail(subject, message, from_email, recipient_list)  

        return redirect('otp', user_id=userregister.id)  # Pass user ID to the OTP verification  

    return render(request, 'signup.html')


def otpverify(request, user_id):  
    try:  
        user = User.objects.get(id=user_id)  
        otp_record = OTP.objects.get(user=user)  
    except (User.DoesNotExist, OTP.DoesNotExist):  
        messages.error(request, 'Invalid verification attempt.')  
        return redirect('signup')  

    if request.method == 'POST':  
        otp_input = request.POST.get('otp', '')  
        if otp_input == otp_record.otp_code:  
            user.is_active = True  
            user.save()  
            otp_record.delete()  # OTP can be deleted after verification  
            messages.success(request, 'Email verified successfully!')  
            return redirect('/signin')  
        else:  
            messages.error(request, 'OTP Not matched! Try again.')  

    return render(request, 'otpverification.html')

def signin(request):  
    if request.method == 'POST':  
        signinname = request.POST.get('signinname')  
        signinpassword = request.POST.get('signinpassword')  

        user = User.objects.filter(username=signinname).first()  
        
        if user and not user.is_active:  
            messages.info(request, 'Your email is not verified!')  
        elif user:  
            userauth = authenticate(username=signinname, password=signinpassword.strip())  
            if userauth:  
                login(request, userauth)  
                return redirect('home')  
            else:  
                messages.error(request, 'Wrong Password! Try again.')  
        else:  
            messages.error(request, 'This user does not exist!')  
    
    return render(request, 'signin.html')

@login_required(login_url='/signin')
def profile(request):
    if request.method == 'POST':
        profilepic = request.FILES.get('profilepic')
    user = User.objects.filter(username = request.user.username).first()
    user_profiles = user.userprofile.all().first()
    userpost = user.user_post.all()
    dic = {
        'userprofile':user_profiles,
        'user':user,
        'userpost':userpost
    }
    return render(request, 'profile.html', dic)
# sco64@428
def addinfo(request):
    if request.method == 'POST':
        profilepic = request.FILES.get('addprofilepic')
        addbio = request.POST.get('addbio')
        print(profilepic, addbio)
        user = User.objects.filter(username = request.user.username).first()
        user.userprofile.create(bio = addbio, profilepic = profilepic)
    return render(request, 'add_info.html')
        
def editinfo(request):
    user = User.objects.filter(username = request.user.username).first()
    userprofiles = user.userprofile.all().first()
    print(userprofiles.bio)
    dic = {'user':user, 'userprofile':userprofiles}
    if request.method == 'POST':  
        profilepic = request.FILES.get('profilepic')  
        username = request.POST.get('username')  
        bio = request.POST.get('bio')
        userprofiles.bio = bio
        if profilepic:
            print('yes, profile picture is available.')
            userprofiles.profilepic = profilepic
            userprofiles.save()
            
          
        print(profilepic, username, bio)
    return render(request, 'editinfo.html', dic)

@login_required(login_url='/signin')
def friends(request):
    return render(request, 'friends.html')

def logoutmethod(request):
    logout(request)
    return redirect('/signin')

@login_required(login_url='/signin')
def add_post(request):
    userinfo = User.objects.filter(username = request.user.username).first()
    userprofile = userinfo.userprofile.all().first()
    
    context = {'userprofile':userprofile}
    if request.method == 'POST':
        aicontent_topic = request.POST.get('aicontent-topic')
        if aicontent_topic:
            import os
            import google.generativeai as genai

            genai.configure(api_key='AIzaSyC4h8jQMwwu5foBgutLkydxXQvdNW3UicM')

            generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            )

            chat_session = model.start_chat(
            history=[
            ]
            )
            response = chat_session.send_message(f'''Reply with short description and important inormation about this topic for a post without extra text or any styles:{aicontent_topic}''')

            # print(response.text)
            chatans = response.text
            messages.info(request, chatans)
        else:
            post_des = request.POST.get('post_description')
            post_img = request.FILES.get('posting')
            if post_img:
                post.objects.create(name = request.user, post_text = post_des, post_pic = post_img)
            else:
                post.objects.create(name = request.user, post_text = post_des)
    return render(request, 'addpost.html', context)