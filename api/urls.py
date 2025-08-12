from django.urls import path
from . import views
#from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView


# API endpoints
urlpatterns =[
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify/<str:code>/', views.verify_batch, name='verify_batch'),
    path('verify/', views.verify_qr_code, name='verify_qr_code'),
]