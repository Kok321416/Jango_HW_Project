from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загружает тестовые данные в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка существующих данных...')
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Данные очищены'))

        # Создаем категории
        categories_data = [
            {
                'name': 'Электроника',
                'description': (
                    'Компьютеры, телефоны, планшеты и другие электронные '
                    'устройства'
                )
            },
            {
                'name': 'Одежда',
                'description': (
                    'Мужская и женская одежда, обувь, аксессуары'
                )
            },
            {
                'name': 'Книги',
                'description': (
                    'Художественная литература, учебники, научные издания'
                )
            },
            {
                'name': 'Спорт',
                'description': (
                    'Спортивный инвентарь, одежда для спорта, тренажеры'
                )
            },
            {
                'name': 'Дом и сад',
                'description': (
                    'Товары для дома, сада и ремонта'
                )
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Создана категория: {category.name}')
            else:
                self.stdout.write(f'Категория уже существует: {category.name}')

        # Создаем продукты
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': (
                    'Современный смартфон с мощным процессором и отличной '
                    'камерой'
                ),
                'category': 'Электроника',
                'price': 99999.99
            },
            {
                'name': 'MacBook Air M2',
                'description': (
                    'Легкий и мощный ноутбук для работы и творчества'
                ),
                'category': 'Электроника',
                'price': 149999.99
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': (
                    'Флагманский смартфон с инновационными функциями'
                ),
                'category': 'Электроника',
                'price': 89999.99
            },
            {
                'name': "Джинсы Levi's",
                'description': (
                    'Классические джинсы из качественного денима'
                ),
                'category': 'Одежда',
                'price': 5999.99
            },
            {
                'name': 'Кроссовки Nike Air Max',
                'description': (
                    'Удобные кроссовки для повседневной носки и спорта'
                ),
                'category': 'Одежда',
                'price': 8999.99
            },
            {
                'name': 'Футболка Adidas',
                'description': (
                    'Спортивная футболка из дышащей ткани'
                ),
                'category': 'Одежда',
                'price': 2999.99
            },
            {
                'name': 'Война и мир',
                'description': (
                    'Классический роман Льва Толстого'
                ),
                'category': 'Книги',
                'price': 1299.99
            },
            {
                'name': 'Python для начинающих',
                'description': (
                    'Учебник по программированию на Python'
                ),
                'category': 'Книги',
                'price': 2499.99
            },
            {
                'name': 'Гарри Поттер и философский камень',
                'description': (
                    'Первая книга серии о юном волшебнике'
                ),
                'category': 'Книги',
                'price': 1899.99
            },
            {
                'name': 'Беговая дорожка',
                'description': (
                    'Профессиональная беговая дорожка для дома'
                ),
                'category': 'Спорт',
                'price': 89999.99
            },
            {
                'name': 'Гантели 10 кг',
                'description': (
                    'Универсальные гантели для силовых тренировок'
                ),
                'category': 'Спорт',
                'price': 2999.99
            },
            {
                'name': 'Велосипед горный',
                'description': (
                    'Горный велосипед для активного отдыха'
                ),
                'category': 'Спорт',
                'price': 45999.99
            },
            {
                'name': 'Кофемашина DeLonghi',
                'description': (
                    'Автоматическая кофемашина для дома'
                ),
                'category': 'Дом и сад',
                'price': 59999.99
            },
            {
                'name': 'Набор отверток',
                'description': (
                    'Профессиональный набор отверток для ремонта'
                ),
                'category': 'Дом и сад',
                'price': 1999.99
            },
            {
                'name': 'Горшки для цветов',
                'description': (
                    'Набор керамических горшков для комнатных растений'
                ),
                'category': 'Дом и сад',
                'price': 3999.99
            }
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'category': categories[prod_data['category']],
                    'price': prod_data['price']
                }
            )
            if created:
                self.stdout.write(f'Создан продукт: {product.name}')
            else:
                self.stdout.write(f'Продукт уже существует: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Загрузка завершена! Создано категорий: '
                f'{Category.objects.count()}, '
                f'продуктов: {Product.objects.count()}'
            )
        )
