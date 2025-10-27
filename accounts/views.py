from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import User

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # creates user, hashes password
            login(request, user)  # auto-login after register
            messages.success(request, "Welcome!")
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        # already logged in — redirect based on role
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard')
        else:
            return redirect('')

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user.is_banned:
                return render(request, 'accounts/banned.html', {"user": user})

            login(request, user)

            # 👇 redirect admin/staff to dashboard, normal users to profile
            if user.is_staff or user.is_superuser:
                return redirect('dashboard')
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    # if banned after login, block access
    if request.user.is_banned:
        return render(request, 'accounts/banned.html', {"user": request.user})

    return render(request, 'accounts/profile.html', {'user_obj': request.user})


@login_required
def profile_edit_view(request):
    if request.user.is_banned:
        return render(request, 'accounts/banned.html', {"user": request.user})

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})



@login_required
def delete_account_view(request):
    # "Delete my account"
    if request.method == "POST":
        request.user.delete()
        messages.warning(request, "Your account has been deleted.")
        return redirect('register')

    # simple confirm page
    return render(request, 'accounts/delete_confirm.html')



@login_required
def password_change_view(request):
    # block banned users too, same rule as profile_edit
    if request.user.is_banned:
        return render(request, 'accounts/banned.html', {"user": request.user})

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # this updates the password AND hashes it
            # keep the user logged in after password change
            update_session_auth_hash(request, user)

            messages.success(request, "Your password has been updated.")
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/password_change.html', {"form": form})