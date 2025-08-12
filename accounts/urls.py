from django.urls import path
from . import views



urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('',views.home_view,name = 'home'),
    path('about/',views.about,name='about'),
    path('m/login/',views.mobile_login_view,name='mobile_login'),
    path('m/signup/',views.mobile_signup_view,name='mobile_signup'),
    path('m/home/',views.mobile_home_view,name='mobile_login'),

]
