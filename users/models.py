from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_ROLES = (
        ('customer', 'Покупатель'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
    )
    
    username = None
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.TextField('Адрес', blank=True)
    role = models.CharField('Роль', max_length=20, choices=USER_ROLES, default='customer')
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.email
    
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    def is_moderator(self):
        return self.role == 'moderator' or self.is_admin()