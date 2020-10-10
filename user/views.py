import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
import json


def hello(request):
    # if request.method == 'GET':
    #     return HttpResponse(content=123, status=200)
    # else:

    data = {"code": 00, "msg": "hello world"}
    # res = HttpResponse(status=200, content=json.dumps(data), content_type='application/json')
    res = JsonResponse(data=data)
    return res


def login(request):
    return render(request, "login.html")


def home(request):
    # 判断cookie是否存在
    if request.COOKIES.get('uid') == '1' and request.COOKIES.get('username') == 'admin'\
            and request.COOKIES.get('pwd') == 'admin':
        return render(request, "home.html")
    else:
        return HttpResponseRedirect('/user/login/')


@api_view(['POST'])
def api_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username is not None and password is not None:
        if username == 'admin' and password == 'admin':
            res = HttpResponseRedirect('/user/home/')
            # HttpResponseRedirect重定向

            # res = render(request, 'home.html', context={"username": username})
            res.set_cookie("uid", "1")
            res.set_cookie("username", "admin")
            res.set_cookie("pwd", "admin")
            return res

        else:
            return render(request, 'error.html', context={"msg": "账号或者密码错误"})

    else:
        return render(request, 'error.html', context={"msg":"账号或者密码必填"})



