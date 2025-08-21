from django.core.management.base import BaseCommand
from django.core.cache import cache
from catalog.models import Product

class Command(BaseCommand):
    help = 'Тестирует работу кеширования'
    
    def handle(self, *args, **options):
        self.stdout.write('🧪 Тестирование кеширования...')
        
        # Тест 1: Проверка подключения к Redis
        try:
            cache.set('test_key', 'test_value', 10)
            test_value = cache.get('test_key')
            if test_value == 'test_value':
                self.stdout.write(self.style.SUCCESS('✅ Redis подключен и работает'))
            else:
                self.stdout.write(self.style.ERROR('❌ Redis не работает корректно'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка Redis: {e}'))
        
        # Тест 2: Кеширование продуктов
        try:
            products = Product.objects.all()[:5]
            cache.set('test_products', products, 60)
            cached_products = cache.get('test_products')
            
            if cached_products is not None:
                self.stdout.write(self.style.SUCCESS('✅ Кеширование продуктов работает'))
            else:
                self.stdout.write(self.style.ERROR('❌ Кеширование продуктов не работает'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка кеширования: {e}'))
        
        # Тест 3: Очистка кеша
        try:
            cache.delete('test_key')
            cache.delete('test_products')
            self.stdout.write(self.style.SUCCESS('✅ Очистка кеша работает'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка очистки кеша: {e}'))
        
        self.stdout.write('🎉 Тестирование завершено!')
