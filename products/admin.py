from django.contrib import admin
from .models import Category, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description', 'brand', 'model']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'discount_price', 'stock', 'is_available')
        }),
        ('Технические характеристики', {
            'fields': ('brand', 'model'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type']
    prepopulated_fields = {'slug': ('name',)}