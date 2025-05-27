from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('dashboard/', views.pharmacy_dashboard, name='dashboard'),
]