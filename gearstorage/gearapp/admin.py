from django.contrib import admin
from .models import Item, ItemCategory, MainCategory, Storage
from django.utils.html import format_html


# Register your models here.
@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('order',)


@admin.register(ItemCategory)
class ItmeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('order',)


@admin.register(Storage)
class ItmeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('order',)


@admin.register(Item)
class ItmeAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'weight',
                    )
    ordering = ('purchase_date',)
    list_filter = ('current_storage',)

    def image_tag(self, obj):
        return format_html('<img src="/{}" style="max-width:200px; max-height:200px"/>'.format(obj.image))

    image_tag.short_description = 'Image'
