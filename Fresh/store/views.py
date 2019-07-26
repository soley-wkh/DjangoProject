import hashlib

from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from .models import *


# md5加密
def md5_encrypt(text):
    m5 = hashlib.md5()
    text = text.encode(encoding='utf-8')
    m5.update(text)
    return m5.hexdigest()


# 校验用户是否登录
def is_login(func):
    def check(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")  # 用户名
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/store/login/')

    return check


# Create your views here.
def register(request):
    """注册"""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            seller = Seller()
            seller.username = username
            seller.nickname = username
            seller.password = md5_encrypt(password)
            seller.save()
            return HttpResponseRedirect('/store/login/')
    return render(request, 'store/register.html', locals())


def login(request):
    """登录"""
    response = render(request, 'store/login.html')
    response.set_cookie('login_from', 'login_page')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if user:
                web_password = md5_encrypt(password)
                cookies = request.COOKIES.get('login_from')
                if user.password == web_password and cookies == 'login_page':
                    response = HttpResponseRedirect('/store/index/')
                    response.set_cookie('username', username)
                    # cookie提供用户id方便其他功能查询
                    response.set_cookie('user_id', user.id)
                    request.session['username'] = username

                    store = Store.objects.filter(user_id=user.id).first()  # 在查询店铺是否存在
                    response.set_cookie('has_store', store.id) if store else response.set_cookie('has_store', '')
                    return response
    return response


@is_login
def index(request):
    """
    1.首页
    2.添加检查账号是否有店铺的逻辑
    """
    # 查询当前用户是谁
    # user_id = request.COOKIES.get("user_id")
    # user_id = int(user_id) if user_id else 0
    # # 通过用户查询店铺是否存在（店铺和用户通过用户的id进行关联）
    # store = Store.objects.filter(user_id=user_id).first()
    # has_store = 1 if store else 0
    return render(request, 'store/index.html')


def base(request):
    return render(request, 'store/index.html')


def forgot_password(request):
    """忘记密码"""
    return render(request, 'store/forgot-password.html')


def logout(request):
    """退出"""
    response = HttpResponseRedirect('/store/login/')
    for k in request.COOKIES:  # 获取当前所有key
        response.delete_cookie(k)
    del request.session['username']
    return response


@is_login
def register_store(request):
    """注册店铺"""
    type_list = StoreType.objects.all()
    if request.method == 'POST':
        post_data = request.POST
        store_name = post_data.get("store_name")
        store_address = post_data.get("store_address")
        store_description = post_data.get("store_description")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")

        # 通过cookie来得到user_id
        user_id = int(request.COOKIES.get("user_id"))
        # 通过request.post得到类型，但是是一个列表
        type_lists = post_data.getlist("type")

        store_logo = request.FILES.get("store_logo")

        # 保存非多对多数据
        store = Store()
        store.store_name = store_name
        store.store_address = store_address
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.user_id = user_id
        store.store_logo = store_logo
        store.save()  # 保存，生成了数据库当中的一条数据
        # 在生成的数据当中添加多对多字段
        for i in type_lists:  # 循环type列表，得到类型id
            store_type = StoreType.objects.get(id=i)  # 查询类型数据
            store.type.add(store_type)  # 添加到类型字段，多对多的映射表
        store.save()  # 保存数据

        response = HttpResponseRedirect('/store/index/')
        response.set_cookie('has_store', store.id)
        return response

    return render(request, 'store/register_store.html', locals())


@is_login
def add_goods(request):
    """添加商品"""

    goods_type_list = GoodsType.objects.all()

    if request.method == 'POST':
        # 获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_image = request.FILES.get("goods_image")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safe_date = request.POST.get("goods_safeDate")
        goods_store = request.COOKIES.get("has_store")

        goods_type = request.POST.get('type')
        print('==============' + goods_type)

        # 开始保存数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_image = goods_image
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safe_date

        ty = GoodsType.objects.get(id=int(goods_type))
        goods.goods_type = ty
        goods.save()

        # 保存多对多数据
        goods.store_id.add(
            Store.objects.get(id=int(goods_store))
        )
        goods.save()
        return HttpResponseRedirect('/store/list_goods/up/')

    return render(request, 'store/add_goods.html', locals())


@is_login
def list_goods(request, state):
    """
    商品列表
    """
    if state == 'up':
        state_num = 1
    else:
        state_num = 0

    keywords = request.GET.get("keywords", "")
    page_num = request.GET.get("page_num", 1)

    # 查询店铺
    store_id = request.COOKIES.get("has_store")
    store = Store.objects.get(id=int(store_id))

    if keywords:
        goods_list = store.goods_set.filter(goods_name__contains=keywords, goods_under=state_num)
    else:
        goods_list = store.goods_set.filter(goods_under=state_num)
    paginator = Paginator(goods_list, 3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, 'store/list_goods.html',
                  {"page": page, "page_range": page_range, "keywords": keywords, "state": state})


@is_login
def goods_detail(request, goods_id):
    """商品详情"""
    goods = Goods.objects.filter(id=goods_id).first()
    return render(request, 'store/goods_detail.html', locals())


@is_login
def update_goods(request, goods_id):
    """修改商品"""
    goods = Goods.objects.filter(id=goods_id).first()

    if request.method == 'POST':
        # 获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safe_date = request.POST.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")

        # 开始保存数据
        goodss = Goods.objects.get(id=int(goods_id))
        goodss.goods_name = goods_name
        goodss.goods_price = goods_price
        goodss.goods_number = goods_number
        goodss.goods_description = goods_description
        goodss.goods_date = goods_date
        goodss.goods_safeDate = goods_safe_date
        if goods_image:
            goodss.goods_image = goods_image
        goodss.save()
        return HttpResponseRedirect('/store/goods_detail/%s' % goods_id)

    return render(request, 'store/update_goods.html', locals())


def goods_state(request, state):
    if state == 'up':
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get("id")
    referer = request.META.get('HTTP_REFERER')
    if id:
        goods = Goods.objects.filter(id=id).first()
        if state == 'del':
            goods.delete()
        else:
            goods.goods_under = state_num
            goods.save()
    return HttpResponseRedirect(referer)


@is_login
def add_goods_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')

        goods_type = GoodsType()
        goods_type.name = name
        goods_type.description = description
        goods_type.logo = logo
        goods_type.save()
        return HttpResponseRedirect('/store/list_goods_type/')

    return render(request, 'store/goods_type_list.html', locals())


# 商品类型管理
@is_login
def list_goods_type(request):
    goods_type_list = GoodsType.objects.all()
    if request.method == 'POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        logo = request.FILES.get("logo")

        goods_type = GoodsType()
        goods_type.name = name
        goods_type.description = description
        goods_type.logo = logo
        goods_type.save()
    return render(request, 'store/goods_type_list.html', locals())


@is_login
def delete_goods_type(request, goods_type_id):
    goods_type = GoodsType.objects.get(pk=goods_type_id)
    goods_type.delete()
    return HttpResponseRedirect('/store/list_goods_type/')
