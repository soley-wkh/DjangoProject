"""Fresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from store.views import GoodsViewSet
from store.views import GoodsTypeViewSet
from user.views import index

router = routers.DefaultRouter()
router.register(r'goods', GoodsViewSet)  # 注册视图
router.register(r'goods_type', GoodsTypeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('store/', include('store.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^API/', include(router.urls)),  # restful 的跟路由
    re_path(r'^api_auth', include('rest_framework.urls')),  # 接口认证
]

urlpatterns += [
    re_path(r'^$', index)
]
