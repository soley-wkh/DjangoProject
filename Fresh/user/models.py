from django.db import models


# Create your models here.
class User(models.Model):
    """用户模型类"""
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField(max_length=32, verbose_name='邮箱')
    phone = models.CharField(max_length=11, verbose_name='联系电话', blank=True, null=True)
    addr = models.CharField(max_length=256, verbose_name='联系地址', blank=True, null=True)

    class Meta:
        db_table = 'f_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Address(models.Model):
    """地址模型类"""
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    class Meta:
        db_table = 'f_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name


class Order(models.Model):
    """订单表
    待支付 1
    待发货 2
    已发货 3
    已收货 4
    （已退货）0
    """
    order_id = models.CharField(max_length=32, verbose_name='id订单编号')
    goods_count = models.IntegerField(verbose_name='商品数量')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='用户')
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE, verbose_name='地址', blank=True, null=True)
    total_price = models.FloatField(verbose_name='总价')
    order_status = models.IntegerField(default=1, verbose_name='订单状态')

    class Meta:
        db_table = 'f_order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class OrderDetail(models.Model):
    """订单详情表"""
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='订单')
    goods_id = models.IntegerField(verbose_name='商品id')
    goods_name = models.CharField(max_length=32, verbose_name='商品名称')
    goods_price = models.FloatField(verbose_name='商品价格')
    goods_number = models.IntegerField(verbose_name='商品购买数量')
    goods_total = models.FloatField(verbose_name='商品总价')
    goods_store = models.IntegerField(verbose_name='商店id')
    goods_image = models.ImageField(verbose_name='商品图片')

    class Meta:
        db_table = 'f_order_detail'
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name
