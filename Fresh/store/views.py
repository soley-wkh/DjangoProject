import hashlib

from django.shortcuts import render
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
        username = request.COOKIES.get("username")  # 用户名
        user_session = request.session.get("username")
        if username and user_session and username == user_session:
            user = Seller.objects.filter(username=username).first()
            if user:
                return func(request, *args, **kwargs)
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
                    response = HttpResponseRedirect('/store/index')
                    response.set_cookie('username', username)
                    request.session['username'] = username
                    return response
    return response


@is_login
def index(request):
    return render(request, 'store/index.html')
