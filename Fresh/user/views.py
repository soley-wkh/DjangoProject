from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from .models import User
from store.models import GoodsType, Goods
from store.views import md5_encrypt


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
    goods = Goods.objects.get(id=goods_id)
    print('++++++++', goods)

    return render(request, 'user/detail.html', locals())
