from django.contrib import admin
from internet_shop.models import Category, Good


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Good)