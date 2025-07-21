from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from manufacturer.models import Drug
#from accounts.decorators import consumer_required  # optional role check

@login_required
def consumer_homepage(request):
    return render(request, 'consumer/homepage.html')

def about(request):
    return render(request,'consumer/about_page.html')

def scan(request):
    query = request.GET.get("code")
    drug = None
    error = None

    if query:
        try:
            drug = Drug.objects.get(qr_code_string=query)
        except Drug.DoesNotExist:
            error = "Invalid or unregistered QR code."

    return render(request, "consumer/scan.html", {"drug": drug, "error": error}) 

def scan_camera(request):
    return render(request, "consumer/scan_camera.html")
