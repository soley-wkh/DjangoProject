# -*- coding:utf-8 -*-
"""
    version: 
    author : wkh
    time   : 2019/7/31 14:39
    file   : serializers.py
    
"""
from rest_framework import serializers

from .models import *


class GoodsSerializer(serializers.ModelSerializer):
    """声明数据"""

    class Meta:
        model = Goods
        fields = '__all__'
        # fields = ['goods_name', 'goods_price', 'goods_image', 'goods_number', 'goods_description', 'goods_type',
        #           'goods_under']


class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    """声明数据"""

    class Meta:
        model = GoodsType
        # fields = '__all__'
        fields = serializers.ALL_FIELDS
        # fields = ['name', 'description', 'logo']
