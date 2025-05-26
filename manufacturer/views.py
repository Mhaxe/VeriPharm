from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import manufacturer_required  # optional role check

@login_required
@manufacturer_required  
def manufacturer_dashboard(request):
    return render(request, 'manufacturer/dashboard.html')
