import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()

from products.models import Category, Product

# Создаем категории
categories = [
    {'name': 'Процессоры Intel', 'category_type': 'processor'},
    {'name': 'Видеокарты NVIDIA', 'category_type': 'videocard'},
    {'name': 'Материнские платы', 'category_type': 'motherboard'},
    {'name': 'Оперативная память', 'category_type': 'memory'},
    {'name': 'SSD накопители', 'category_type': 'storage'},
    {'name': 'Блоки питания', 'category_type': 'power'},
    {'name': 'Корпуса', 'category_type': 'case'},
    {'name': 'Кулеры', 'category_type': 'cooler'},
    {'name': 'Периферия', 'category_type': 'other'},
]

for cat_data in categories:
    slug = cat_data['name'].lower().replace(' ', '-')
    Category.objects.get_or_create(
        name=cat_data['name'],
        category_type=cat_data['category_type'],
        slug=slug
    )

# Создаем тестовые товары
test_products = [
    {
        'name': 'Процессор Intel Core i7-12700K',
        'slug': 'intel-core-i7-12700k',
        'category': Category.objects.get(name='Процессоры Intel'),
        'description': '12-ядерный процессор Intel Core i7 для игр и профессиональных задач',
        'price': 29999,
        'stock': 10,
        'brand': 'Intel',
        'model': 'Core i7-12700K'
    },
    {
        'name': 'Видеокарта NVIDIA GeForce RTX 4070',
        'slug': 'nvidia-geforce-rtx-4070',
        'category': Category.objects.get(name='Видеокарты NVIDIA'),
        'description': 'Игровая видеокарта с поддержкой трассировки лучей DLSS 3',
        'price': 59999,
        'discount_price': 54999,
        'stock': 5,
        'brand': 'NVIDIA',
        'model': 'RTX 4070'
    },
    {
        'name': 'Материнская плата ASUS ROG STRIX Z790',
        'slug': 'asus-rog-strix-z790',
        'category': Category.objects.get(name='Материнские платы'),
        'description': 'Игровая материнская плата для процессоров Intel 12-13 поколения',
        'price': 32999,
        'stock': 8,
        'brand': 'ASUS',
        'model': 'ROG STRIX Z790'
    },
    {
        'name': 'Оперативная память Kingston Fury 32GB DDR5',
        'slug': 'kingston-fury-32gb-ddr5',
        'category': Category.objects.get(name='Оперативная память'),
        'description': 'Высокоскоростная оперативная память DDR5 6000MHz',
        'price': 12999,
        'stock': 15,
        'brand': 'Kingston',
        'model': 'Fury Beast 32GB'
    },
    {
        'name': 'SSD накопитель Samsung 980 Pro 1TB',
        'slug': 'samsung-980-pro-1tb',
        'category': Category.objects.get(name='SSD накопители'),
        'description': 'Высокоскоростной NVMe SSD для игр и профессиональных задач',
        'price': 8999,
        'discount_price': 7999,
        'stock': 20,
        'brand': 'Samsung',
        'model': '980 Pro 1TB'
    },
]

for prod_data in test_products:
    Product.objects.get_or_create(**prod_data)

print("Тестовые данные созданы успешно!")