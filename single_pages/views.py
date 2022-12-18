from django.shortcuts import render
from shoppingmall.models import Item

# Create your views here.
def home(request):
    recent_item = Item.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/home.html', {
        'recent_items' : recent_item,
    })

def about_us(request):
    return render(request, 'single_pages/about_us.html')

def mypage(request):
    return render(request, 'single_pages/mypage.html')