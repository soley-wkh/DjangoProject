# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/7/22 14:16
    file   : urls.py
    
"""
from django.urls import path, re_path
from . import views

app_name = 'store'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    re_path(r'^$', views.index, name='index'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout, name='logout'),
    path('register_store/', views.register_store, name='register_store'),
    path('add_goods/', views.add_goods, name='add_goods'),
    path('list_goods/', views.list_goods, name='list_goods'),
]

urlpatterns += [
    path('base/', views.base, name='base'),
]
