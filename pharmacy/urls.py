from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('dashboard/', views.pharmacy_dashboard, name='dashboard'),
    path('verify/<int:distribution_id>/', views.verify_receipt, name='verify_receipt'),
]