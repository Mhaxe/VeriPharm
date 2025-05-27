from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import pharmacy_required

@login_required
@pharmacy_required  
def pharmacy_dashboard(request):
    return render(request, 'pharmacy/dashboard.html')