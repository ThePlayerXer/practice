
from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Ожидание'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )
    
    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
        ('online', 'Онлайн-оплата'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True
    )
    order_number = models.CharField('Номер заказа', max_length=20, unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес доставки')
    city = models.CharField('Город', max_length=100)
    postal_code = models.CharField('Почтовый индекс', max_length=20)
    
    status = models.CharField('Статус', max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_METHODS, default='card')
    payment_completed = models.BooleanField('Оплачено', default=False)
    
    total_price = models.DecimalField('Итоговая цена', max_digits=10, decimal_places=2)
    discount = models.DecimalField('Скидка', max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField('Стоимость доставки', max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            self.order_number = ''.join(random.choices(string.digits, k=10))
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField('Название товара', max_length=200)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
    
    def get_total_price(self):
        return self.price * self.quantity