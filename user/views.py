import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json

from xlrd import xldate_as_tuple

from util import *
from django.contrib import auth
import xlrd
from user.models import *
from django.db import connection
from datetime import datetime


def init_db(request):
    # 1、excel 读取回来
    # 读第一个sheet
    workbook = xlrd.open_workbook("./图书信息表.xlsx")
    sheet = workbook.sheet_by_name("作者信息")
    Author.objects.all().delete()
    AuthorDetail.objects.all().delete()
    Publisher.objects.all().delete()
    Book.objects.all().delete()
    cursor = connection.cursor()
    sql1 = "UPDATE sqlite_sequence SET seq = 0 WHERE name='user_author';"
    sql2 = "UPDATE sqlite_sequence SET seq = 0 WHERE name='user_authordetail';"
    sql3 = "UPDATE sqlite_sequence SET seq = 0 WHERE name='user_publisher';"
    sql4 = "UPDATE sqlite_sequence SET seq = 0 WHERE name='user_book';"
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.close()
    for i in range(1, sheet.nrows):
        print(sheet.row_values(i))
        data = sheet.row_values(i)
        author = Author.objects.create(name=data[0])
        if data[1] == '男':
            data[1] = 1
        else:
            data[1] = 0
        AuthorDetail.objects.create(sex=data[1], age=data[2], email=data[3], phone_number=data[4], author=author)

    # 读第2个sheet，完成出版社信息的新增
    sheet2 = workbook.sheet_by_name("出版社信息")
    for i in range(1, sheet2.nrows):
        data2 = sheet2.row_values(i)
        Publisher.objects.create(name=data2[0], address=data2[1], city=data2[2], website=data2[3])

        # 读第3个sheet，完成图书信息的新增
    sheet3 = workbook.sheet_by_name("图书信息")
    for i in range(1, sheet3.nrows):
        data3 = sheet3.row_values(i)
        publish = Publisher.objects.filter(name=data3[2])
        d = datetime(*xldate_as_tuple(data3[3], 0))
        book = Book.objects.create(name=data3[0], publish=publish[0], publish_date=d, price=data3[4])

        for name in data3[1].split(','):
            author = Author.objects.filter(name=name).first()
            book.author.add(author)

    return HttpResponse(123)


def hello(request):
    # if request.method == 'GET':
    #     return HttpResponse(content=123, status=200)
    # else:

    data = {"code": 00, "msg": "hello world"}
    # # res = HttpResponse(status=200, content=json.dumps(data), content_type='application/json')
    res = JsonResponse(data)
    return res

    # res = HttpResponse()
    # res.set_cookie('id', 123)
    # return res


def login(request):
    return render(request, "login.html")


def home(request):
    # 判断cookie是否存在
    username = request.COOKIES.get('username')
    # noinspection PyBroadException
    try:
        pwd = request.get_signed_cookie('pwd')
    except:
        pwd = None

    if is_login(username, pwd):
        return render(request, "home.html", {"username": username})
    else:
        return HttpResponseRedirect('/user/login/')


@api_view(['POST'])
def api_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    is_cookie = request.POST.get('is_login')
    print(is_cookie)

    # auth.authenticate(username=username,password=password)

    if username is not None and password is not None:
        is_av = is_login(username, password)

        if is_av is not None:
            res = HttpResponseRedirect('/user/home/')
            # HttpResponseRedirect重定向
            # res = render(request, 'home.html', context={"username": username})
            if is_cookie == 'on':
                res.set_cookie("uid", is_av, max_age=86400)
                res.set_cookie("username", username, max_age=86400)
                res.set_signed_cookie("pwd", password, max_age=86400)
                return res
            else:
                res.set_cookie("uid", is_av)
                res.set_cookie("username", username)
                res.set_signed_cookie("pwd", password)
                return res

        else:
            return render(request, 'error.html', context={"msg": "账号或者密码错误"})

    else:
        return render(request, 'error.html', context={"msg": "账号或者密码必填"})


@api_view(['GET', 'POST'])
def api_logout(request):
    res = HttpResponseRedirect('/user/login/')
    res.delete_cookie('uid')
    res.delete_cookie('username')
    res.delete_cookie('pwd')
    return res
