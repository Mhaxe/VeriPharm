from django.urls import path
from . import views

app_name = 'consumer'

urlpatterns = [
    path('homepage/', views.consumer_homepage, name='consumer_home'),
    path('about/',views.about,name = 'about'),
    path('scan/', views.scan, name='scan'),
    path("scan-camera/", views.scan_camera, name="scan_camera"),
    
]
