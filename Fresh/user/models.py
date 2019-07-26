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
