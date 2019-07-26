# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/7/25 13:56
    file   : urls.py
    
"""
from django.urls import path

from . import views
from .views import RegisterView, LoginView

app_name = 'user'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='regist'),  # 注册
    path('login/', LoginView.as_view(), name='login'),  # 登录
    path('logout/', views.logout, name='logout'),  # 退出
    path('index/', views.index, name='index'),  # 首页
    path('goods_list/', views.goods_list, name='goods_list'),  # 商品列表
    path('detail/', views.detail, name='detail'),  # 商品详情

]
urlpatterns += [
    path('base/', views.base)
]
