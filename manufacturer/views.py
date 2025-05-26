from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import manufacturer_required 
from accounts.views import logout

@login_required
@manufacturer_required  
def manufacturer_dashboard(request):
    if request.method == 'POST' and 'logout_button' in request.POST:
        print("logout")
        logout(request)
        return redirect('home')
    return render(request, 'manufacturer/dashboard.html')
