from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request,'hhome.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = request.POST.get('role','consumer')
            user.save()
            login(request, user)
            return redirect('consumer:consumer_home') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'hhome.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            role = user.role
            login(request, user)
            if role == 'consumer':
                return redirect('consumer:consumer_home')
            elif role == 'manufacturer':
                return redirect('manufacturer:dashboard')
            elif role == 'pharmacist':
                return redirect('pharmacy:dashboard')
            elif role == 'distributor':
                return redirect('distributor:dashboard')
            else:
                return redirect('dashboard')#to be changed to an error page i guess
            
    else:
        form = CustomLoginForm()
    return render(request, 'hhome.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def consumer_homepage(request):
    render(request,'chp.html')

