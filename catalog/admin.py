from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Product
    """
    list_display = ['name', 'price', 'is_published', 'is_active', 'owner', 'created_at']
    list_filter = ['is_published', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_published']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_published')
        }),
        ('Владелец', {
            'fields': ('owner',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем владельца при создании через админку"""
        if not change:  # Если это создание нового объекта
            obj.owner = request.user
        super().save_model(request, obj, form, change)


        
