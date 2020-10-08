from pickle import GET

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['GET', 'POST'])
def hello(request):
    # GET 
    print(request.path)
    print(request.method)
    if request.method == 'GET':
        username = request.GET.get('username')
        pwd = request.GET.get('pwd')

        if username is not None and pwd is not None:
            return render(request, 'mail.html', context={"name": username})

        else:
            return render(request, 'error.html', context={"msg": "用户名或者密码错误！！"})

    else:
        # request.method == 'POST':
        username = request.POST.get('username')  # POST方法是 url encode 方式
        pwd = request.POST.get("pwd")

    # elif:
    #     try:
    #         data = json.loads(request.body)  # json格式请求入参
    #
    #     except:
    #         return render(request, 'error.html', context={"msg": "请求格式非json格式"})
    #
    #     print(data)
    #     username = data.get('username')
    #     pwd = data.get('pwd')

        # print(request.FILES)
        # username = request.FILES.get(' mayflies ').name  # 获取文件名称
        # print(username)
        # request.COOKIES.get('token')

        # print(request.COOKIES)
        # return HttpResponse(123)
        if username is not None and pwd is not None:
            return render(request, 'mail.html', context={"name": username})

        else:
            return render(request, 'error.html', context={"msg": "用户名或者密码错误！！"})
