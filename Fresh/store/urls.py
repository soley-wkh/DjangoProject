# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/7/22 14:16
    file   : urls.py
    
"""
from django.urls import path,re_path
from . import views

app_name = 'store'
urlpatterns = [
    path('register/', views.register,name=''),
    path('login/', views.login),
    path('index/', views.index),
    re_path(r'^$', views.index),
]
