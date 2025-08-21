from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product
from .services import ProductService

@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    """Очищает кеш при изменении или удалении продукта"""
    # Очищаем кеш всех продуктов
    ProductService.clear_all_products_cache()
    
    # Если у продукта есть категория, очищаем кеш категории
    if hasattr(instance, 'category_id') and instance.category_id:
        ProductService.clear_category_cache(instance.category_id)

@receiver(post_save, sender=Product)
def clear_product_detail_cache(sender, instance, **kwargs):
    """Очищает кеш детальной страницы продукта при изменении"""
    # Очищаем кеш страницы продукта
    cache_key = f'product_detail_{instance.pk}'
    cache.delete(cache_key)