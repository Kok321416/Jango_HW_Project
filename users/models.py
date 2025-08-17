from django.db import models
from django.contrib.auth.models import AbstractUser

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