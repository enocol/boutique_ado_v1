from django.contrib import admin
from .models import Category, Product

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')
    search_fields = ('friendly_name', 'name')

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku', 'name', 'category', 'price', 'rating', 'image'
    )

    ordering = ('sku',)
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
