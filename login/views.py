from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request,'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('consumer_homepage') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            role = user.role
            login(request, user)
            if role == 'consumer':
                return redirect('consumer_home')
            elif role == 'manufacturer':
                return redirect('manufacturer_home')
            elif role == 'pharmacist':
                return redirect('pharmacist_home')
            elif role == 'admin':
                return redirect('admin_home')
            else:
                return redirect('dashboard')#to be changed to an error page i guess
            
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def consumer_homepage(request):
    render(request,'chp.html')

