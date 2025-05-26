from django.urls import path
from . import views

app_name = 'manufacturer'

urlpatterns = [
    path('manufacturer/dashboard/', views.manufacturer_dashboard, name='dashboard'),
]
