from django.urls import path
from . import views

app_name = 'users'  # Пространство имен для приложения

urlpatterns = [
    # URL для регистрации
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # URL для авторизации
    path('login/', views.UserLoginView.as_view(), name='login'),
    
    # URL для выхода
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
