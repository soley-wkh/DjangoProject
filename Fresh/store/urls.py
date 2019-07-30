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
    re_path(r'list_goods/(?P<state>\w+)', views.list_goods, name='list_goods'),
    re_path(r'^goods_detail/(?P<goods_id>\d+)', views.goods_detail, name='goods_detail'),
    re_path(r'^update_goods/(?P<goods_id>\d+)', views.update_goods, name='update_goods'),
    re_path(r'goods_state/(?P<state>\w+)', views.goods_state, name='goods_state'),
    path('list_goods_type/', views.list_goods_type, name='list_goods_type'),  # 商品类型列表
    path('delete_goods_type/<int:goods_type_id>', views.delete_goods_type, name='delete_goods_type'),  # 删除商品类型
    path('add_goods_type/', views.add_goods_type, name='add_goods_type'),  # 添加商品类型

    re_path(r'order_list/(?P<status>\d+)', views.order_list, name='order_list'),  # 订单列表
    re_path(r'order_status/(?P<status>\d+)', views.order_status, name='order_status'),  # 订单状态
]

urlpatterns += [
    path('base/', views.base, name='base'),
]
