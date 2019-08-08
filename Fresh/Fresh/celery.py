# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/8/1 20:01
    file   : celery.py
    
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置celery执行的环境变量，执行Django项目的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fresh.settings')

# 创建celery应用
app = Celery('CeleryTask')  # celery应用的名称
app.config_from_object('django.conf:settings')  # 加载的配置文件

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
