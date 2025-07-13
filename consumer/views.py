from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
#from accounts.decorators import consumer_required  # optional role check

@login_required
def consumer_homepage(request):
    return render(request, 'consumer/homepage.html')

def about(request):
    return render(request,'consumer/about_page.html')


