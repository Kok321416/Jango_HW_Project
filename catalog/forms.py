from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Константы с запрещенными словами (в любом регистре)
BANNED_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа", 
    "дешево", "бесплатно", "обман", "полиция", "радар"
]

class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов
    Включает валидацию запрещенных слов и цены
    """
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'is_active']
        
        # Настройка виджетов для полей
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название продукта'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Введите описание продукта'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0',
                    'placeholder': '0.00'
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            )
        }
        
        # Настройка лейблов полей
        labels = {
            'name': 'Название продукта',
            'description': 'Описание продукта', 
            'price': 'Цена (руб.)',
            'is_active': 'Продукт активен'
        }
        
        # Настройка help_text для полей
        help_texts = {
            'name': 'Введите название продукта (максимум 100 символов)',
            'description': 'Подробно опишите продукт',
            'price': 'Укажите цену в рублях',
            'is_active': 'Отметьте, если продукт доступен для продажи'
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с дополнительной стилизацией
        Этот метод вызывается при создании экземпляра формы
        """
        super().__init__(*args, **kwargs)
        
        # Дополнительная стилизация для всех полей
        for field_name, field in self.fields.items():
            # Добавляем CSS классы для всех полей
            if field_name != 'is_active':  # Исключаем чекбокс
                field.widget.attrs.update({
                    'class': 'form-control mb-3'
                })
            
            # Специальная стилизация для чекбокса
            if field_name == 'is_active':
                field.widget.attrs.update({
                    'class': 'form-check-input me-2'
                })

    def clean_name(self):
        """
        Валидация названия продукта на запрещенные слова
        Этот метод автоматически вызывается Django при валидации поля 'name'
        """
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError('Название продукта обязательно для заполнения')
        
        # Проверяем на запрещенные слова (в любом регистре)
        name_lower = name.lower()
        
        for banned_word in BANNED_WORDS:
            if banned_word in name_lower:
                raise ValidationError(
                    f'Название продукта не может содержать запрещенное слово "{banned_word}"'
                )
        
        return name

    def clean_description(self):
        """
        Валидация описания продукта на запрещенные слова
        Этот метод автоматически вызывается Django при валидации поля 'description'
        """
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError('Описание продукта обязательно для заполнения')
        
        # Проверяем на запрещенные слова (в любом регистре)
        description_lower = description.lower()
        
        for banned_word in BANNED_WORDS:
            if banned_word in description_lower:
                raise ValidationError(
                    f'Описание продукта не может содержать запрещенное слово "{banned_word}"'
                )
        
        return description

    def clean_price(self):
        """
        Кастомная валидация для поля цены
        Проверяет, что цена не может быть отрицательной
        """
        price = self.cleaned_data.get('price')
        
        if price is None:
            raise ValidationError('Цена продукта обязательна для заполнения')
        
        if price < 0:
            raise ValidationError('Цена продукта не может быть отрицательной')
        
        if price == 0:
            raise ValidationError('Цена продукта не может быть равной нулю')
        
        return price

        
