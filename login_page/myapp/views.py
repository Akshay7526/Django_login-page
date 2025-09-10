from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        
        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)  # hashes password automatically
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')
    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')  
        password = request.POST.get('password')  

        if not username or not password:
            messages.error(request, "Both fields are required.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, "login.html")

def profile_view(request):
    return render(request,"profile.html")


def home_view(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        # Create User
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.save()

        # Create Profile with extra fields
        Profile.objects.create(user=user, gender=gender, surname=last_name)

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')
    return render(request, "signup.html")