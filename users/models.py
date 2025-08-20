from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    '''
    Кастомная модель пользователя
    '''
    username = None  # Убираем поле username, так как будем использовать email
    email = models.EmailField(
        unique=True,
        verbose_name="Email адрес",
        help_text="Введите ваш email адрес"
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватарка',
        help_text='Загрузите вашу изображение для аватара',
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        verbose_name='Телефон',
        help_text='Введите ваш номер телефона',
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        help_text='Введите вашу страну',
        blank=True,
        null=True
    )

    # Указываем, что email является полем для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Поля, обязательные для создания суперпользователя (email уже обязателен)
    
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users_user'

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email