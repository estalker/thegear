from django.contrib import admin
from .models import Item, ItemCategory, MainCategory

# Register your models here.
@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('order',)


@admin.register(ItemCategory)
class ItmeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('order',)


@admin.register(Item)
class ItmeAdmin(admin.ModelAdmin):
    list_display = ('brand','name', 'damaged')
    ordering = ('purchase_date',)