from django.urls import path
from mail import views


urlpatterns = [
    path('hello/', views.hello),
]
