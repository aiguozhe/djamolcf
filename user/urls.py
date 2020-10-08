from django.urls import path
from user import views


urlpatterns = [
    path('hello/', views.hello),
    path('login/', views.login),
    path('api/login/', views.api_login),
]