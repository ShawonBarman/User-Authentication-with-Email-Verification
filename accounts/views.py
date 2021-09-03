from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def homepage(request):
    return render(request, "home.html")

def login_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_object = User.objects.filter(username = username).first()
        if user_object is None:
            messages.success(request, 'User not found.')
            return redirect("login_attempt")
        profile_object = Profile.objects.filter(user = user_object).first()
        if profile_object.is_varified == False:
            messages.success(request, 'Account not verified, check your mail.')
            return redirect("login_attempt")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login_attempt')

        login(request, user)
        return redirect('home')
    return render(request, "login.html")

def regiser_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(username, email, password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is already taken.')
                return redirect('register_attempt')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is already taken.')
                return redirect('register_attempt')

            # create a user object
            user_object = User.objects.create(username = username, email = email)
            user_object.set_password(password)
            user_object.save()

            auth_token = str(uuid.uuid4())
            # create a profile object for that user
            profile_object = Profile.objects.create(user = user_object, auth_token = auth_token)
            profile_object.save()

            send_mail_for_verification(email, auth_token)

            return redirect("token_send")
        except Exception as e:
            print(e)


    return render(request, "register.html")

def success(request):
    return render(request, "success.html")

def token_send(request):
    return render(request, "token_send.html")

def verification(request, auth_token):
    try:
        profile_object = Profile.objects.filter(auth_token = auth_token).first()
        if profile_object:
            if profile_object.is_varified:
                messages.success(request, 'Your account is already verified.')
                return redirect("login_attempt")
            profile_object.is_varified = True
            profile_object.save()
            messages.success(request, 'Congratulation, your account has been verified.')
            return redirect("login_attempt")
        else:
            return redirect("/error")

    except Exception as e:
        print(e)
        return redirect("home")

def send_mail_for_verification(email, token):
    subject = "Your account need to be verified"
    message = f"Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}"
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)

def error_page(request):
    return render(request, "error.html")