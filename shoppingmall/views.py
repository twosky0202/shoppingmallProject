from django.shortcuts import render, redirect
from .models import Item, Manufacturer, Category, Color, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
# from rest_framework import viewsets
# from .serializers import postSerializer

def delete_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    item = comment.item
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        PermissionDenied

class ItemUpdate(LoginRequiredMixin,UpdateView):
    model = Item
    fields = ['name', 'content', 'image', 'price', 'manufacturer', 'category']

    template_name = 'shoppingmall/item_update_form.html'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user == self.get_object().author:
    #         return super(ItemUpdate,self).dispatch(request, *args, **kwargs)
    #     else:
    #         raise PermissionDenied

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        response = super(ItemUpdate,self).form_valid(form)
        self.object.colors.clear()
        colors_str = self.request.POST.get('colors_str')
        if colors_str:
            colors_str = colors_str.strip()
            colors_str = colors_str.replace(',', ';')
            color_list = colors_str.split(';')
            for c in color_list:
                c = c.strip()
                color, is_color_created = Color.objects.get_or_create(name=c)
                if is_color_created:
                    color.slug = slugify(c, allow_unicode=True)
                    color.save()
                self.object.colors.add(color)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemUpdate,self).get_context_data()
        if self.object.colors.exists:
            color_str_list = list()
            for c in self.object.colors.all():
                color_str_list.append(c.name)
            context['color_str_default'] = ';'.join(color_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        return context

class ItemCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Item
    fields = ['name', 'content', 'image', 'price', 'manufacturer', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemCreate,self).form_valid(form)
            colors_str = self.request.POST.get('colors_str')
            if colors_str:
                colors_str = colors_str.strip()
                colors_str = colors_str.replace(',', ';')
                color_list = colors_str.split(';')
                for c in color_list:
                    c = c.strip()
                    color, is_color_created = Color.objects.get_or_create(name=c)
                    if is_color_created:
                        color.slug = slugify(c, allow_unicode=True)
                        color.save()
                    self.object.colors.add(color)
            return response
        else:
            return redirect('/shoppingmall/')


class ItemList(ListView):
    model = Item
    ordering = '-pk'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList, self).get_context_data()
        context['manufacturers'] = Manufacturer.objects.all()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        return context

class ItemSearch(ItemList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(Q(name__contains=q) | Q(colors__name__contains=q)).distinct()
        return item_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemDetail, self).get_context_data()
        context['manufacturers'] = Manufacturer.objects.all()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context

def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()

                return redirect(comment.get_absolute_url())
        else: # GET
            return redirect(item.get_absolute_url())
    else: # 로그인 안한 사용자
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def manufacturer_page(request, slug):
    manufacturer = Manufacturer.objects.get(slug=slug)
    item_list = Item.objects.filter(manufacturer=manufacturer)

    return render(request, 'shoppingmall/item_list.html', {
        'manufacturer' : manufacturer,
        'item_list' : item_list,
        'manufacturers' : Manufacturer.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count,
        'categories': Category.objects.all(),
    })

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
        'no_category_item_count' : Item.objects.filter(category=None).count,
        'manufacturers': Manufacturer.objects.all(),
    })

def color_page(request, slug):
    color = Color.objects.get(slug=slug)
    item_list = color.item_set.all()
    return render(request, 'shoppingmall/item_list.html', {
        'color': color,
        'item_list': item_list,
        'colors': Color.objects.all(),
        'no_color_item_count': Item.objects.filter(colors=None).count,
        'manufacturers': Manufacturer.objects.all(),
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count,
    })