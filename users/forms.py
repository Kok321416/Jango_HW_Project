from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # Получаем нашу кастомную модель пользователя

class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя
    Наследуется от UserCreationForm, которая предоставляет поля password1 и password2
    """
    
    class Meta:
        model = User  # Указываем нашу модель пользователя
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Стилизация всех полей
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control mb-3'
            })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован')
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Не устанавливаем username, так как он не используется в нашей модели
        
        if commit:
            user.save()
        
        return user

class UserLoginForm(AuthenticationForm):
    """
    Форма для авторизации пользователя
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Переименовываем поле username в email
        self.fields['username'].label = 'Email'
        self.fields['username'].help_text = 'Введите ваш email адрес'
        
        # Стилизация всех полей
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control mb-3'
            })
