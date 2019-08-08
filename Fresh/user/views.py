import time
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from .models import User
from store.models import GoodsType, Goods, Store
from .models import Order
from .models import OrderDetail
from .models import Address
from .models import Cart
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
        good_list = goods_type.goods_set.filter(goods_under=1).values()[:4]  # 查询前4条数据
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


from django.core.cache import cache


# 商品详情
def detail(request):
    goods_data = cache.get('goods_data')
    if goods_data:
        goods = goods_data
    else:
        goods_id = request.GET.get('goods_id')
        if goods_id:
            goods_data = Goods.objects.filter(id=goods_id).first()
            if goods_data:
                cache.set('goods_data', goods_data, 2 * 60)
                goods = goods_data
                return render(request, 'user/detail.html', locals())
    # goods_id = request.GET.get('goods_id')
    # if goods_id:
    #     goods = Goods.objects.filter(id=goods_id).first()
    #     if goods:
    #         return render(request, 'user/detail.html', locals())
    return HttpResponse('该商品已下架')


def cart(request):
    '''购物车'''
    return render(request, 'user/cart.html')


def set_order_id(user_id, goods_id, store_id):
    timestr = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return timestr + str(user_id) + str(goods_id) + str(store_id)


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
        order_id = request.GET.get("order_id")
        if order_id:
            order = Order.objects.get(id=order_id)
            details = order.orderdetail_set.all()
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


def cart(request):
    """购物车"""
    user_id = request.COOKIES.get('user_id')
    goods_lst = Cart.objects.filter(user_id=user_id)

    if request.method == 'POST':
        post_data = request.POST
        cart_data = []  # 收集前端传递过来的数据
        for k, v in post_data.items():
            if k.startswith("goods_"):
                cart_data.append(Cart.objects.get(id=int(v)))
        goods_count = len(cart_data)  # 提交过来的数据总的数量
        goods_total = sum([int(i.goods_total) for i in cart_data])  # 订单总价

        # 修改使用聚类查询返回指定商品的总价
        # 1、查询到所有的商品
        cart_data = []  # 收集前端传递过来的商品的id
        for k, v in post_data.items():
            if k.startswith("goods_"):
                cart_data.append(int(v))
        # 2、使用 in方法进行范围的划定，然后使用Sum方法进行计算
        cart_goods = Cart.objects.filter(id__in=cart_data).aggregate(Sum("goods_total"))  # 获取到总价
        print(cart_goods)

        # 保存订单
        order = Order()
        # 订单当中有多个商品或多个店铺，使用goods_count来代替商品id，用2代替店铺id
        order.order_id = set_order_id(user_id, goods_count, '2')
        order.goods_count = goods_count
        order.user = User.objects.get(id=user_id)
        order.total_price = goods_total
        order.order_status = 1
        order.save()

        # 保存订单详情
        for detail in cart_data:
            order_detail = OrderDetail()
            order_detail.order = order  # 是一条订单数据
            order_detail.goods_id = detail.goods_id
            order_detail.goods_name = detail.goods_name
            order_detail.goods_price = detail.goods_price
            order_detail.goods_total = detail.goods_total
            order_detail.goods_number = detail.goods_number
            order_detail.goods_store = detail.goods_store
            order_detail.goods_image = detail.goods_image
            order_detail.save()

        url = "/user/place_order/?order_id=%s" % order.id
        return HttpResponseRedirect(url)

    return render(request, 'user/cart.html', locals())


def add_cart(request):
    """添加购物车"""
    ret = {"state": "error", "data": ""}
    if request.method == 'POST':
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        goods = Goods.objects.get(id=int(goods_id))
        user_id = request.COOKIES.get("user_id")

        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price * count
        cart.goods_number = count
        cart.goods_image = goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store.id
        cart.user_id = user_id
        cart.save()
        ret["state"] = 'success'
        ret["data"] = '商品添加成功'
    else:
        ret["data"] = "请求错误"
    return JsonResponse(ret)


import datetime


def TestGoods(request):
    goods_type = GoodsType.objects.all()
    sg = "杏、樱桃、桃、水蜜桃、油桃、黑莓、覆盆子、云莓、罗甘莓、白里叶莓、橘子、砂糖桔、橙子、柠檬、青柠、柚子、金桔、葡萄柚、香橼、佛手、指橙、黄皮果、蟠桃、李子、梅子、青梅、西梅、白玉樱桃"
    znyr = "猪肉、猪腿、大肠、羊肉、羊蹄、羊头、羊杂、牛板筋、牛肉、牛排"
    hxsc = "巴沙鱼、虾仁、三文鱼、长尾鳕、白虾、北极甜虾、大黄鱼、海鳝鱼、美国红黑虎虾"
    qldl = "乌骨鸡、绿壳蛋乌鸡、榛鸡、黑凤鸡、白来航鸡、安得纽夏鸡、黑米诺卡鸡、洛岛红鸡、黑狼山鸡、新汗夏、芦花鸡、浅花苏塞克斯、澳洲黑、九斤黄鸡、七彩山鸡"
    store = Store.objects.get(id=1)
    for f in sg.split("、"):
        goods = Goods()
        goods.goods_name = f
        goods.goods_price = 25.0
        goods.goods_image = "store/img/page_1_3.jpg"
        goods.goods_number = 100
        goods.goods_description = f
        goods.goods_date = datetime.datetime.now()
        goods.goods_safeDate = 1
        goods.goods_under = 1
        goods.goods_type = goods_type[0]
        goods.store = store
        goods.save()
    for z in znyr.split("、"):
        goods = Goods()
        goods.goods_name = z
        goods.goods_price = 25.0
        goods.goods_image = "store/img/page_1_6.jpg"
        goods.goods_number = 100
        goods.goods_description = z
        goods.goods_date = datetime.datetime.now()
        goods.goods_safeDate = 1
        goods.goods_under = 1
        goods.goods_type = goods_type[1]
        goods.store = store
        goods.save()
    for h in hxsc.split("、"):
        goods = Goods()
        goods.goods_name = h
        goods.goods_price = 25.0
        goods.goods_image = "store/img/page_1_18.jpg"
        goods.goods_number = 100
        goods.goods_description = h
        goods.goods_date = datetime.datetime.now()
        goods.goods_safeDate = 1
        goods.goods_under = 1
        goods.goods_type = goods_type[2]
        goods.store = store
        goods.save()
    for q in qldl.split("、"):
        goods = Goods()
        goods.goods_name = q
        goods.goods_price = 25.0
        goods.goods_image = "store/img/page_2_15.jpg"
        goods.goods_number = 100
        goods.goods_description = q
        goods.goods_date = datetime.datetime.now()
        goods.goods_safeDate = 1
        goods.goods_under = 1
        goods.goods_type = goods_type[3]
        goods.store = store
        goods.save()
    return HttpResponse("ok")


from django.core.mail import send_mail
from django.conf import settings


def send_email(request):
    recver = """3392279511@qq.com,
    215558997@qq.com,
    773733859@qq.com,
    912575770@qq.com,
    1529825704@qq.com,
    1307128051@qq.com,
    721788741@qq.com,
    3303236612@qq.com,
    710731910@qq.com,
    329688391@qq.com,
    626978318@qq.com,
    419538402@qq.com,
    1637805820@qq.com,
    738389368@qq.com,
    329688391@qq.com,
    1225858108@qq.com,
    329688391@qq.com,
    452341999@qq.com,
    1225858108@qq.com"""

    html_message = '<h1>欢迎您成为***注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/">http://127.0.0.1:8000/user/active/</a>'

    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_FROM,
        recver.split(",\n"),
        html_message=html_message
    )
    return HttpResponse('ok')


from CeleryTask.tasks import add


def get_add(request):
    add.delay(2, 3)
    return JsonResponse({'status': 200})


# def small_white_views(request):
#     print("我是小白视图")
#     raise TypeError("我就不想好好的")
#     return HttpResponse("我是小白视图")

def small_white_views(request):
    # print("我是小白视图")

    rep = HttpResponse("I am rep")
    rep.render = lambda: HttpResponse("hello world")
    return rep

# def small_white_views(request):
#     # print("我是小白视图")
#     def hello():
#         return HttpResponse("hello world")
#     rep = HttpResponse("I am rep")
#     rep.render = hello
#     return rep

# def small_white_views(request):
#     print("我是小白视图")
#     def render():
#         print("hello world")
#         return HttpResponse("98k")
#     rep = HttpResponse("od")
#     rep.render = render
#     return rep
