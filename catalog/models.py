from django.db import models

# Create your models here.
class Product(models.Model):
    """
    Модель продукта для хранения информации о товарах
    """
    name = models.CharField(
        max_length=100, 
        verbose_name="Название продукта",
        help_text="Введите название продукта"
    )
    description = models.TextField(
        verbose_name="Описание продукта",
        help_text="Введите описание продукта"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта",
        help_text="Введите цену продукта"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.price} руб."
    