from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.conf import settings
import requests

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username Already Taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Email being used ")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                    # auth.login(request,user)
                    # messages.success(request,"You are now logged in")
                    # return redirect('index')
                    user.save()
                    messages.success(request,"You are now registered you can login now ")
                    return redirect('login')



        else:
            messages.error(request,'Passwords Do not Match')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        })
        result = response.json()
        if result.get('success'):
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "You are now logged in")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid Credentials")
        else:
            messages.error(request, "reCAPTCHA validation failed")
        return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,"You are now Logged Out")
        return redirect('index')

    
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts':user_contacts
    }
    return render(request,'accounts/dashboard.html',context)
