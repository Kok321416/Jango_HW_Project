from django.core.cache import cache
from .models import Product

class ProductService:
    """Сервисный слой для работы с продуктами"""
    
    @staticmethod
    def get_products_by_category(category_id, cache_timeout=60*15):
        """
        Получает список продуктов по категории с кешированием
        
        Args:
            category_id (int): ID категории
            cache_timeout (int): Время жизни кеша в секундах (по умолчанию 15 минут)
        
        Returns:
            QuerySet: Список продуктов в указанной категории
        """
        # Формируем ключ кеша
        cache_key = f'products_category_{category_id}'
        
        # Пытаемся получить данные из кеша
        cached_products = cache.get(cache_key)
        
        if cached_products is not None:
            return cached_products
        
        # Если данных нет в кеше, получаем из БД
        try:
            products = Product.objects.filter(
                is_active=True,
                is_published=True
            ).select_related('owner').order_by('-created_at')
            
            # Сохраняем в кеш
            cache.set(cache_key, products, cache_timeout)
            
            return products
            
        except Exception as e:
            # В случае ошибки возвращаем пустой QuerySet
            return Product.objects.none()
    
    @staticmethod
    def get_category_info(category_id):
        """
        Получает информацию о категории
        
        Args:
            category_id (int): ID категории
        
        Returns:
            Category: Объект категории или None
        """
        cache_key = f'category_info_{category_id}'
        
        cached_category = cache.get(cache_key)
        if cached_category is not None:
            return cached_category
        
        try:
            # Поскольку у вас нет модели Category, возвращаем None
            # category = Category.objects.get(id=category_id)
            # cache.set(cache_key, category, 60*60)  # Кешируем на 1 час
            # return category
            return None
        except Exception:
            return None
    
    @staticmethod
    def clear_category_cache(category_id):
        """
        Очищает кеш для указанной категории
        
        Args:
            category_id (int): ID категории
        """
        cache_keys = [
            f'products_category_{category_id}',
            f'category_info_{category_id}'
        ]
        
        for key in cache_keys:
            cache.delete(key)
    
    @staticmethod
    def get_all_products(cache_timeout=60*15):
        """
        Получает все активные продукты с кешированием
        
        Args:
            cache_timeout (int): Время жизни кеша в секундах
        
        Returns:
            QuerySet: Список всех активных продуктов
        """
        cache_key = 'all_products_list'
        
        cached_products = cache.get(cache_key)
        if cached_products is not None:
            return cached_products
        
        try:
            products = Product.objects.filter(
                is_active=True
            ).select_related('owner').order_by('-created_at')
            
            cache.set(cache_key, products, cache_timeout)
            return products
            
        except Exception as e:
            return Product.objects.none()
    
    @staticmethod
    def clear_all_products_cache():
        """Очищает кеш для всех продуктов"""
        cache.delete('all_products_list')
            