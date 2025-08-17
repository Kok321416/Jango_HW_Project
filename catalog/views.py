from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm

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
    """
    Представление для отображения списка всех продуктов
    Наследуется от Django Generic View для списков
    """
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Переопределяем queryset для фильтрации только активных продуктов
        """
        return Product.objects.filter(is_active=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительный контекст в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список продуктов'
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о продукте
    Наследуется от Django Generic View для детального просмотра
    Требует авторизации пользователя
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
        
        return response
    
    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительный контекст в шаблон
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление продукта: {self.object.name}'
        return context    
    
