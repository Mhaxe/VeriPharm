from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import distro_required  # optional role check

@login_required
@distro_required  
def distro_dashboard(request):
    return render(request, 'distro/dashboard.html')