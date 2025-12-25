from django.db import models
from django.urls import reverse

class Category(models.Model):
    CATEGORY_TYPES = (
        ('processor', 'Процессоры'),
        ('videocard', 'Видеокарты'),
        ('motherboard', 'Материнские платы'),
        ('memory', 'Оперативная память'),
        ('storage', 'Накопители'),
        ('power', 'Блоки питания'),
        ('case', 'Корпуса'),
        ('cooler', 'Кулеры'),
        ('other', 'Другое'),
    )
    
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    category_type = models.CharField('Тип категории', max_length=20, choices=CATEGORY_TYPES)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField('Количество на складе')
    is_available = models.BooleanField('Доступен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    
    brand = models.CharField('Бренд', max_length=100, blank=True)
    model = models.CharField('Модель', max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    def get_final_price(self):
        """Возвращает окончательную цену (со скидкой если есть)"""
        return self.discount_price if self.discount_price else self.price
    
    def get_discount_percent(self):
        """Возвращает процент скидки"""
        if self.discount_price and self.price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return int(discount)
        return 0