from django.urls import path
from . import views

app_name = 'distributor'

urlpatterns = [
    path('dashboard/', views.distributor_dashboard, name='dashboard'),
]