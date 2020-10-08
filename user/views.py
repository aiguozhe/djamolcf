import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
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


# @api_view(['GET', 'POST'])
def api_login(request):
    # global res
    username = ''
    password = ''

    # if request.method == 'GET':
    #     username = request.GET.get('username')
    #     password = request.GET.get('password')
    #
    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    if username is not None and password is not None:
        if username == 'admin' and password == 'admin':
            res = render(request, 'home.html', context={"username": username})
            # res.set_cookie("cookies","1234")
            return 11

       else:
            return render(request, 'error.html', context={"msg": "账号或者密码错误"})

    else:
        return render(request, 'error.html', context={"msg":"账号或者密码必填"})



