from django.urls import path
from . import views

app_name = 'distro'

urlpatterns = [
    path('distro/dashboard/', views.distro_dashboard, name='dashboard'),
]