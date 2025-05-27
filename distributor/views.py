from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import distributor_required  # optional role check

@login_required
@distributor_required  
def distributor_dashboard(request):
    return render(request, 'distributor/dashboard.html')