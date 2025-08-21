from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.conf import settings
from .models import Product
from .forms import ProductForm
from .services import ProductService

def home(request):
    """
    Главная страница с списком всех активных продуктов
    """
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'products': products,
        'title': 'Главная страница'
    }
    
    return render(request, 'home.html', context)

def contact(request):
    """
    Страница контактов
    """
    context = {
        'title': 'Контакты'
    }
    return render(request, 'contacts.html', context)

class ProductListView(ListView):
    """Представление для отображения списка всех продуктов с кешированием"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        """Получаем кешированный список продуктов"""
        # Используем сервисный слой для получения продуктов
        return ProductService.get_all_products()
    
    def get_context_data(self, **kwargs):
        """Добавляем дополнительный контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список продуктов'
        
        # Добавляем информацию о кешировании для отладки
        if settings.DEBUG:
            cache_key = 'all_products_list'
            cache_info = cache.get(cache_key)
            context['cache_info'] = {
                'is_cached': cache_info is not None,
                'cache_key': cache_key
            }
        
        return context

@method_decorator(cache_page(60*15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о продукте
    Наследуется от Django Generic View для детального просмотра
    Требует авторизации пользователя
    Кешируется на 15 минут
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительный контекст в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Продукт: {self.object.name}'
        return context

class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Представление для создания нового продукта
    Наследуется от Django Generic View для создания объектов
    SuccessMessageMixin добавляет сообщения об успешном создании
    Требует авторизации пользователя
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    success_message = "Продукт '%(name)s' успешно создан!"
    
    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительный контекст в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового продукта'
        context['button_text'] = 'Создать продукт'
        return context

    def form_valid(self, form):
        """Автоматически устанавливаем владельца при создании"""
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        
        # Очищаем кеш после создания продукта
        ProductService.clear_all_products_cache()
        
        return response

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление для редактирования существующего продукта
    Наследуется от Django Generic View для обновления объектов
    Требует авторизации пользователя
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    success_message = "Продукт '%(name)s' успешно обновлен!"
    
    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительный контекст в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование продукта: {self.object.name}'
        context['button_text'] = 'Сохранить изменения'
        return context

    def dispatch(self, request, *args, **kwargs):
        """Проверяем права доступа перед выполнением"""
        obj = self.get_object()
        
        # Проверяем, является ли пользователь владельцем или модератором
        if obj.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            return HttpResponseForbidden("У вас нет прав для редактирования этого продукта")
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Очищаем кеш после обновления продукта"""
        response = super().form_valid(form)
        ProductService.clear_all_products_cache()
        return response

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления продукта
    Наследуется от Django Generic View для удаления объектов
    Требует авторизации пользователя
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    
    def delete(self, request, *args, **kwargs):
        """
        Переопределяем метод удаления для добавления сообщения об успехе
        """
        # Получаем объект перед удалением для сообщения
        product = self.get_object()
        
        # Вызываем родительский метод удаления
        response = super().delete(request, *args, **kwargs)
        
        # Добавляем сообщение об успешном удалении
        messages.success(request, f"Продукт '{product.name}' успешно удален!")
        
        # Очищаем кеш после удаления продукта
        ProductService.clear_all_products_cache()
        
        return response

    def dispatch(self, request, *args, **kwargs):
        """Проверяем права доступа перед выполнением"""
        obj = self.get_object()
        
        # Проверяем, является ли пользователь владельцем или модератором
        if obj.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            return HttpResponseForbidden("У вас нет прав для удаления этого продукта")
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительный контекст в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление продукта: {self.object.name}'
        return context

class UnpublishProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden("У вас нет прав для отмены публикации")
        
        product.is_published = False
        product.save()
        messages.success(request, f"Продукт '{product.name}' снят с публикации")
        
        # Очищаем кеш после изменения статуса публикации
        ProductService.clear_all_products_cache()
        
        return redirect('catalog:product_detail', pk=pk)

class CategoryProductsView(ListView):
    """Представление для отображения продуктов по категории"""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        """Получаем продукты по категории через сервисный слой"""
        category_id = self.kwargs.get('category_id')
        return ProductService.get_products_by_category(category_id)
    
    def get_context_data(self, **kwargs):
        """Добавляем информацию о категории в контекст"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        
        # Получаем информацию о категории через сервис
        category = ProductService.get_category_info(category_id)
        
        if category:
            context['category'] = category
            context['title'] = f'Продукты в категории: {category.name}'
        else:
            context['category'] = None
            context['title'] = 'Категория не найдена'
        
        return context


