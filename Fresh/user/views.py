import time
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from .models import User
from store.models import GoodsType, Goods
from .models import Order
from .models import OrderDetail
from .models import Address
from store.views import md5_encrypt

from alipay import AliPay


# 校验用户是否登录
def is_login(func):
    def check(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")  # 用户名
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/user/login/')

    return check


def base(request):
    return render(request, 'user/base.html')


@is_login
def index(request):
    """首页"""
    result_list = []
    goods_type_list = GoodsType.objects.all()  # 查询所有类型
    for goods_type in goods_type_list:
        good_list = goods_type.goods_set.values()[:4]  # 查询前4条数据
        if good_list:
            result_list.append({
                'id': goods_type.id,
                'name': goods_type.name,
                'description': goods_type.description,
                'logo': goods_type.logo,
                'goods_list': good_list
            })  # 构建查询结果
    return render(request, 'user/index.html', {'result_list': result_list})


# user/register
class RegisterView(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        user = User()
        user.username = username
        user.password = md5_encrypt(password)
        user.email = email
        user.save()

        return HttpResponseRedirect('/user/login/')


# user/login
class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if all([username, password]):
            user = User.objects.filter(username=username).first()
            if user:
                if user.password == md5_encrypt(password):
                    response = HttpResponseRedirect('/user/index/')
                    response.set_cookie('username', user.username)
                    request.session['username'] = user.username
                    response.set_cookie('user_id', user.id)
                    return response
        return render(request, 'user/login.html')


# 退出
def logout(request):
    response = HttpResponseRedirect('/user/login/')
    # 删除所有的请求携带的cookies
    for key in request.COOKIES:
        response.delete_cookie(key)
    # 删除session
    del request.session['username']
    return response


# 商品列表
def goods_list(request):
    """列表页"""
    goods_lst = []
    type_id = request.GET.get('type_id')
    # 获取类型
    goods_type = GoodsType.objects.filter(id=type_id).first()
    if goods_type:
        goods_lst = goods_type.goods_set.filter(goods_under=1)
    return render(request, 'user/goods_list.html', locals())


# 商品详情
def detail(request):
    goods_id = request.GET.get('goods_id')
    if goods_id:
        goods = Goods.objects.filter(id=goods_id).first()
        if goods:
            return render(request, 'user/detail.html', locals())
    return HttpResponse('该商品已下架')


def cart(request):
    '''购物车'''
    return render(request, 'user/cart.html')


def set_order_id(user_id, goods_id, store_id):
    timestr = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return timestr + user_id + goods_id + store_id


def place_order(request):
    '''结算'''
    if request.method == 'POST':
        # post数据
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")

        # cookie的数据
        user_id = request.COOKIES.get('user_id')

        # 数据库的数据
        goods = Goods.objects.get(id=goods_id)
        store_id = goods.store.id
        price = goods.goods_price

        order = Order()
        order.order_id = set_order_id(str(user_id), str(goods_id), str(store_id))
        order.goods_count = count
        order.user = User.objects.get(id=user_id)
        order.total_price = count * price
        order.order_status = 1
        order.save()

        order_detail = OrderDetail()
        order_detail.order = order
        order_detail.goods_id = goods_id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_price = goods.goods_price
        order_detail.goods_number = count
        order_detail.goods_total = count * goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_image = goods.goods_image
        order_detail.save()

        details = [order_detail]

        return render(request, 'user/place_order.html', locals())
    else:
        return HttpResponse("非法请求")


def pay_order(request):
    '''支付订单'''

    money = request.GET.get('money')
    order_id = request.GET.get('order_id')

    alipay = AliPay(
        appid=settings.APPID,
        app_notify_url=None,
        app_private_key_string=str(settings.APP_PRIVATE_KEY_STRING),  # 必须转字符串(不然报错)
        alipay_public_key_string=str(settings.ALIPAY_PUBLIC_KEY_STRING),  # 必须转字符串(不然报错)
        sign_type='RSA2'
    )

    # 发起支付请求
    order_str = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject='生鲜交易',  # 交易主题
        return_url="http://127.0.0.1:8000/user/pay_result/",
        notify_url="http://127.0.0.1:8000/user/pay_result/"
    )

    order = Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_str)


def pay_result(request):
    """支付结果
    支付宝支付成功自动用get请求返回的参数
    #编码
    charset=utf-8
    #商家订单号
    out_trade_no=10002
    #订单类型
    method=alipay.trade.page.pay.return
    #订单金额
    total_amount=1000.00
    #校验值
    sign=enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D
    #订单号
    trade_no=2019072622001422161000050134
    #用户的应用id
    auth_app_id=2016093000628355
    #版本
    version=1.0
    #商家的应用id
    app_id=2016093000628355
    #加密方式
    sign_type=RSA2
    #商家id
    seller_id=2088102177891440
    #时间
    timestamp=2019-07-26
    """
    return render(request, 'user/pay_result.html', locals())


class UserInfoView(View):
    def get(self, request):
        return render(request, 'user/user_center_info.html', {'page': 'user'})


class UserOrderView(View):
    def get(self, request):
        return render(request, 'user/user_center_order.html', {'page': 'order'})


class AddressView(View):
    def get(self, request):
        user = request.user
        print(user)
        return render(request, 'user/user_center_site.html', {'page': 'address'})

    def post(self, request):
        # 接收数据
        receiver = request.POST.get("receiver")
        addr = request.POST.get("addr")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")


        address = Address()

        return HttpResponseRedirect(reverse('user:address'))
