from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import UserRegistrationForm, UserLoginForm
from .models import User

class RegisterView(FormView):
    """
    Представление для регистрации нового пользователя
    """
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        messages.success(self.request, f'Добро пожаловать, {user.get_full_name()}! Регистрация прошла успешно.')
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш магазин!'
        message = f"""
        Здравствуйте!
        
        Добро пожаловать в наш интернет-магазин!
        
        Ваш аккаунт успешно создан.
        Email: {user_email}
        
        Спасибо за регистрацию!
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

class UserLoginView(LoginView):
    """
    Представление для авторизации пользователя
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')

class UserLogoutView(LogoutView):
    """
    Представление для выхода пользователя
    """
    next_page = reverse_lazy('catalog:home')
