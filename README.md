# Django HW Project

Веб-приложение на Django для домашнего задания.

## 📋 Описание проекта

Это Django проект с базовой структурой, включающий:
- Главную страницу (`home/`)
- Страницу контактов (`contacts/`)
- Административную панель Django
- Приложение `catalog` для управления контентом

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

### Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <url-репозитория>
   cd Jango_HW_Project
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   ```

3. **Активируйте виртуальное окружение:**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Установите зависимости:**
   ```bash
   pip install django
   ```

5. **Выполните миграции базы данных:**
   ```bash
   python manage.py migrate
   ```

6. **Создайте суперпользователя (опционально):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```

8. **Откройте браузер и перейдите по адресу:**
   ```
   http://127.0.0.1:8000/
   ```

## 📁 Структура проекта

```
Jango_HW_Project/
├── catalog/                 # Основное приложение
│   ├── __init__.py
│   ├── admin.py            # Административная панель
│   ├── apps.py             # Конфигурация приложения
│   ├── models.py           # Модели данных
│   ├── urls.py             # URL маршруты приложения
│   ├── views.py            # Представления (views)
│   ├── tests.py            # Тесты
│   └── templates/          # HTML шаблоны
│       └── home.html       # Шаблон главной страницы
├── config/                 # Конфигурация проекта
│   ├── __init__.py
│   ├── settings.py         # Настройки Django
│   ├── urls.py             # Главные URL маршруты
│   ├── asgi.py             # ASGI конфигурация
│   └── wsgi.py             # WSGI конфигурация
├── manage.py               # Утилита управления Django
├── .gitignore              # Исключения для Git
└── README.md               # Документация проекта
```

## 🌐 Доступные страницы

- **Главная страница:** `http://127.0.0.1:8000/home/`
- **Контакты:** `http://127.0.0.1:8000/contacts/`
- **Админ панель:** `http://127.0.0.1:8000/admin/`

## ⚙️ Настройки

Основные настройки проекта находятся в файле `config/settings.py`:

- **DEBUG:** `True` (для разработки)
- **ALLOWED_HOSTS:** `["*"]` (разрешает все хосты)
- **DATABASE:** SQLite3 (по умолчанию)
- **STATIC_URL:** `"static/"`
- **STATICFILES_DIRS:** `(BASE_DIR / "static",)`

## 🛠️ Разработка

### Добавление новых страниц

1. Создайте новое представление в `catalog/views.py`:
   ```python
   def new_page(request):
       return render(request, 'new_page.html')
   ```

2. Добавьте URL маршрут в `catalog/urls.py`:
   ```python
   path('new-page/', new_page, name='new_page')
   ```

3. Создайте HTML шаблон в `catalog/templates/new_page.html`

### Создание моделей

1. Определите модель в `catalog/models.py`
2. Создайте миграцию: `python manage.py makemigrations`
3. Примените миграцию: `python manage.py migrate`

## 🧪 Тестирование

Для запуска тестов используйте:
```bash
python manage.py test
```

## 📦 Развертывание

### Продакшн настройки

1. Измените `DEBUG = False` в `config/settings.py`
2. Настройте `ALLOWED_HOSTS` для вашего домена
3. Настройте статические файлы:
   ```bash
   python manage.py collectstatic
   ```

### Рекомендуемые настройки для продакшна

- Используйте PostgreSQL вместо SQLite
- Настройте HTTPS
- Используйте переменные окружения для секретных ключей
- Настройте логирование

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект создан в образовательных целях.

## 📞 Поддержка

Если у вас есть вопросы или проблемы, создайте Issue в репозитории.

## 🔄 Версии

- **Django:** 5.2.3
- **Python:** 3.8+

---

**Автор:** [Ваше имя]  
**Дата создания:** 2024 