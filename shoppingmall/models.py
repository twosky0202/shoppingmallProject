from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os.path

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
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
    content = MarkdownxField()  # 설명
    image = models.ImageField(upload_to='shoppingmall/images/')  # 이미지
    price = models.IntegerField()  # 가격
    created_at = models.DateField(auto_now_add=False, null=True, blank=True)  # 제조년월

    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL)  # 제조사
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # 카테고리
    colors = models.ManyToManyField(Color, blank=True)  # 색상


    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
           return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1399/b76ae05ef96b24c0/svg/{self.author.email}'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/shoppingmall/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.item.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
           return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1399/b76ae05ef96b24c0/svg/{self.author.email}'