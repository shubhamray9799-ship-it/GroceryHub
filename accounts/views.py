from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
import random

from .models import UserProfile


# ------------------------------
# REGISTER USER
# ------------------------------
def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "accounts/register.html")

        # Phone already registered?
        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")
            return render(request, "accounts/register.html")

        # Create Django user (password saved securely)
        user = User.objects.create_user(
            username=phone,
            email=email,
            password=password,
            first_name=name
        )

        # Create your own user profile
        UserProfile.objects.create(
            user=user,
            phone=phone,
            name=name,
            email=email
        )

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "accounts/register.html")



# ------------------------------
# LOGIN WITH PASSWORD
# ------------------------------
def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = authenticate(request, username=phone, password=password)

        if user is not None:
            login(request, user)
            return redirect("home_page")
        else:
            messages.error(request, "Invalid phone or password")

    return render(request, "accounts/login.html")



# ------------------------------
# LOGIN WITH OTP
# ------------------------------
def login_otp_view(request):
    phone = ""
    otp_input = ""

    if request.method == "POST":
        phone = request.POST.get("phone")
        otp_input = request.POST.get("otp")

        # STEP 1 — Generate OTP when user clicks "Get OTP"
        if not otp_input:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['otp_phone'] = phone
            messages.success(request, f"Your OTP is: {otp}")  # For testing
            return render(request, "accounts/login_otp.html", {"phone": phone})

        # STEP 2 — Verify OTP
        saved_otp = request.session.get('otp')
        saved_phone = request.session.get('otp_phone')

        if saved_otp == otp_input and saved_phone == phone:

            # Find or create user
            user, created = User.objects.get_or_create(username=phone)

            # If user is new → create profile
            if created:
                UserProfile.objects.create(
                    user=user,
                    phone=phone,
                    name="New User",
                    email=""
                )

            login(request, user)

            # Clear OTP session
            del request.session['otp']
            del request.session['otp_phone']

            return redirect("home")

        messages.error(request, "Invalid OTP")

    return render(request, "accounts/login_otp.html", {"phone": phone})