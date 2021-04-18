from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('videos/videoComment', views.videoComment, name='videoComment'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.SignUp, name='SignUp'),
    path('login/', views.LogIn, name='LogIn'),
    path('logout/', views.LogOut, name='LogOut'),
    path('about/', views.about, name='about'),
    path('videos/', views.allsubject, name='allsubject'),
    path('search/', views.search, name='search'),
    path('videos/<str:slug>', views.pvideos, name='pvideos'),
]