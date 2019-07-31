# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/7/25 13:56
    file   : urls.py
    
"""
from django.urls import path, re_path

from . import views

# from .views import RegisterView, LoginView

app_name = 'user'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),  # 注册
    path('login/', views.LoginView.as_view(), name='login'),  # 登录
    path('logout/', views.logout, name='logout'),  # 退出
    path('index/', views.index, name='index'),  # 首页
    path('goods_list/', views.goods_list, name='goods_list'),  # 商品列表
    path('detail/', views.detail, name='detail'),  # 商品详情
    path('cart/', views.cart, name='cart'),  # 购物车
    path('place_order/', views.place_order, name='place_order'),  # 结算
    path('pay_order/', views.pay_order, name='pay_order'),  # 支付
    path('pay_result/', views.pay_result, name='pay_result'),  # 支付结果

    re_path(r'^$', views.UserInfoView.as_view(), name='user'),  # 用户中心信息页
    path('order/', views.UserOrderView.as_view(), name='order'),  # 用户中心订单页
    path('address/', views.AddressView.as_view(), name='address'),  # 用户中心地址页
    path('cart/', views.cart, name='cart'),  # 购物车
    path('add_cart/', views.add_cart, name='add_cart'),  # 添加购物车

]
urlpatterns += [
    path('base/', views.base),
    # path("TestGoods/", views.TestGoods),
]
