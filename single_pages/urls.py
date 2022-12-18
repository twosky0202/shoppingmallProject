from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about_us/', views.about_us),
    path('mypage/', views.mypage),
]