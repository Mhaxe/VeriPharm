from django.urls import path
from . import views

app_name = 'manufacturer'

urlpatterns = [
    path('manufacturer/dashboard/', views.manufacturer_dashboard, name='dashboard'),
    path('scan/', views.scan, name='scan'),
    path('records/', views.manufacturer_records, name='records'),
    path('about/', views.about, name='about'),
    path("scan-camera/", views.scan_camera, name="scan_camera"),
]
