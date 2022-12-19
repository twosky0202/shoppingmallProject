from django.shortcuts import render
from shoppingmall.models import Item, Manufacturer, Category, Color, Comment


# Create your views here.
def home(request):
    recent_items = Item.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/home.html', {
        'recent_items' : recent_items,
    })

def about_us(request):
    manufacturers = Manufacturer.objects.all()
    categories = Category.objects.all()
    colors = Color.objects.all()

    manufacturer_list = [["Name", "Count"], ]
    for m in manufacturers:
        manufacturer_list.append([m.name, Item.objects.filter(manufacturer=m).count()])

    category_list = [["Name", "Count"], ]
    for category in categories:
        category_list.append([category.name, Item.objects.filter(category=category).count()])

    color_list = [["Name", "Count"], ]
    for colors in colors:
        color_list.append([colors.name, Item.objects.filter(colors=colors).count()])

    return render(request, 'single_pages/about_us.html', {
        'manufacturer_list': manufacturer_list,
        'category_list': category_list,
        'color_list': color_list,
    })

def mypage(request):
    # comments = Comment.objects.all()

    return render(request, 'single_pages/mypage.html')

