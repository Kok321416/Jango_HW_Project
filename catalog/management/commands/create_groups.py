from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы и назначает им права доступа'

    def handle(self, *args, **options):
        # Получаем тип контента для модели Product
        content_type = ContentType.objects.get_for_model(Product)
        
        # Создаем группу "Модератор продуктов"
        moderators_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        
        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')
        
        # Получаем все необходимые разрешения
        permissions_to_add = [
            'can_unpublish_product',  # Кастомное право
            'delete_product',         # Удаление любого продукта
            'change_product',         # Изменение любого продукта
            'view_product',           # Просмотр продуктов
        ]
        
        # Добавляем разрешения в группу
        for perm_codename in permissions_to_add:
            try:
                permission = Permission.objects.get(
                    codename=perm_codename,
                    content_type=content_type
                )
                moderators_group.permissions.add(permission)
                self.stdout.write(f'Разрешение {perm_codename} добавлено в группу')
            except Permission.DoesNotExist:
                self.stdout.write(f'Разрешение {perm_codename} не найдено')
        
        self.stdout.write(self.style.SUCCESS('Группы и разрешения успешно настроены!'))