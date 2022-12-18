from django.shortcuts import render, redirect
from .models import Item, Manufacturer, Category, Color
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
# from .forms import CommentForm
# from django.shortcuts import get_object_or_404
# from django.db.models import Q
# from rest_framework import viewsets
# from .serializers import postSerializer

class ItemList(ListView):
    model = Item
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        return context

class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        return context

def category_page(request, slug):
    if slug == 'no_category' :
        category = '기타'
        item_list = Item.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        item_list = Item.objects.filter(category=category)
    return render(request, 'shoppingmall/item_list.html', {
        'category' : category,
        'item_list' : item_list,
        'categories' : Category.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count
    })

def color_page(request, slug):
    color = Color.objects.get(slug=slug)
    item_list = color.post_set.all()
    return render(request, 'shoppingmall/item_list.html', {
        'color' : color,
        'item_list' : item_list,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count
    })