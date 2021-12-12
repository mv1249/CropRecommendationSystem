from django.contrib import admin
from django.urls import path
from CropApp import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.homepage, name='homepage'),
    path('createaccount/', views.createaccount, name='createaccount'),
    path('recommend/', views.recommend, name='recommend'),
    path('yeild/', views.yeild, name='yeild'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('blog/', views.blog, name='blog'),
    path('blogcontent/', views.blogcontent, name='blogcontent'),


]
