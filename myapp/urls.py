from django.urls import path
from .views import *

urlpatterns=[
    path('home',Home.as_view(),name='home'),
    path('contact',Contact.as_view(),name='contact'),
    path('about',About.as_view(),name='about'),
    path('registration',RegistrationView.as_view(),name='registration'),
    path('login',Login.as_view(),name='login'),
    path('registernow',RegisterNow.as_view(),name='registernow'),
    path('logout',logoutpage,name='logout'),
    path('forget_password',ForgetPassword.as_view(),name='forget_password'),
    path('dashboard',dashboard,name='dashboard'),
    path('profile',profile,name='profile'),
    path('editprofile',EditProfile.as_view(),name='editprofile'),
    path('change_password',change_password,name='change_password'),
    path('adminpage',adminpage,name='adminpage'),
    path('adminedit/<int:id>',adminedit,name='adminedit'),
    path('deactivate/<int:id>',deactivate,name='deactivate'),
    path('activate/<int:id>',activate,name='activate'),
    path('displayall/<int:id>',displayall,name='displayall'),
    path('adddetails',AddDetails.as_view(),name='addetails')
]