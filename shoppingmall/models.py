from django.db import models
from django.contrib.auth.models import User
import os.path

class Color(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shoppingmall/color/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shoppingmall/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Manufacturer(models.Model):
    name = models.CharField(max_length=50)  # 제조사명
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    address = models.TextField()  # 주소
    contact = models.CharField(max_length=30)  # 연락처
    introduction = models.TextField()  # 제조사 소개

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shoppingmall/manufacturer/{self.slug}/'


class Item(models.Model):
    name = models.CharField(max_length=50)  # 상품명
    content = models.TextField()  # 설명
    image = models.ImageField(upload_to='shoppingmall/images/', blank=True)  # 이미지
    price = models.IntegerField()  # 가격
    created_at = models.DateField(auto_now_add=True)  # 제조년월

    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.SET_NULL)  # 제조사
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # 카테고리
    color = models.ManyToManyField(Color, blank=True)  # 색상

    def __str__(self):
        return f'[{self.manufacturer}] {self.name}'

    def get_absolute_url(self):
        return f'/shoppingmall/{self.pk}/'
