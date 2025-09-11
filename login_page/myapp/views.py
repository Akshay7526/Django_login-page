from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')

        # Use email as username
        username = email

        if User.objects.filter(username=username).exists():
            messages.error(request, "An account with this email already exists")
            return redirect('signup')

        # Create User
        user = User.objects.create_user(
            username=username,  # same as email
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.save()

        # Create Profile
        Profile.objects.create(
            user=user,
            gender=gender,
            first_name=first_name,
            last_name=last_name
        )

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


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":   # when form submitted (edit)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    # Show edit mode only if ?edit=1 in the URL
    edit_mode = request.GET.get("edit") == "1"

    return render(
        request,
        "profile.html",
        {"form": form, "profile": profile, "edit_mode": edit_mode}
    )



@login_required
def home_view(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect('login')
