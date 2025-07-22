from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('dashboard/', views.pharmacy_dashboard, name='dashboard'),
    path('verify/<int:distribution_id>/', views.verify_receipt, name='verify_receipt'),
    path('scan/', views.scan, name='scan'),
    path("scan-camera/", views.scan_camera, name="scan_camera"),
]