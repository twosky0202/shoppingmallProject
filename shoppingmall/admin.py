from django.contrib import admin
from .models import Item, Manufacturer, Category, Color

admin.site.register(Item)

class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
admin.site.register(Manufacturer, ManufacturerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
admin.site.register(Category, CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
admin.site.register(Color, ColorAdmin)