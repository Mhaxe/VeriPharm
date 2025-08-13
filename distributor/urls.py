from django.urls import path
from . import views

app_name = 'distributor'

urlpatterns = [
    path('dashboard/', views.distributor_dashboard, name='dashboard'),
    path('verify/<int:distribution_id>/', views.verify_distribution, name='verify_distribution'),
    path('pass/',views.pass_to_pharmacy,name = 'pass_to_pharmacy'),
    path('about/',views.about,name = 'about'),
    path('scan/', views.scan, name='scan'),
    path("scan-camera/", views.scan_camera, name="scan_camera"),
    path('download-qr/<int:batch_id>/', views.download_batch_qr, name='download_batch_qr'),

]