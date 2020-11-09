from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(unique=True, max_length=10)
    password = models.CharField(null=False, max_length=10)
    sex = models.IntegerField(choices=((0, '女'), (1, '男')), default=0)


# 作者表
class Author(models.Model):
    name = models.CharField(max_length=30, null=False)


# 作者详情表
class AuthorDetail(models.Model):
    sex = models.IntegerField(choices=((0, '女'), (1, '男')), null=False)
    age = models.IntegerField(null=False)
    phone_number = models.CharField(max_length=13, null=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    author = models.OneToOneField(Author, on_delete=models.CASCADE)


# 出版社表
class Publisher(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    address = models.CharField(max_length=30, unique=True, null=False)
    city = models.CharField(max_length=30, null=False)
    website = models.URLField(max_length=100, unique=True, null=False)


# 书籍表
class Book(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    publish_date = models.DateField(null=False)
    price = models.FloatField(null=False)
    publish = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ManyToManyField(Author)
