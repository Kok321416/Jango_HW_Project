# Миграция с SQLite на PostgreSQL

## Выполненные шаги:

### 1. Обновление зависимостей
- ✅ `psycopg2` уже был установлен в `requirements.txt`

### 2. Обновление настроек Django
- ✅ Изменен `ENGINE` с `django.db.backends.sqlite3` на `django.db.backends.postgresql`
- ✅ Настроены параметры подключения к PostgreSQL

### 3. Создание базы данных
- ✅ Создана база данных `jango_hw_project` в PostgreSQL
- ✅ Создан пользователь `django_user` с паролем `django123`

### 4. Очистка старых данных
- ✅ Удален файл `db.sqlite3`
- ✅ Удалены старые миграции

### 5. Создание новых миграций
- ✅ Выполнена команда `python manage.py makemigrations`
- ✅ Созданы миграции для приложений `catalog` и `blog_app`

### 6. Применение миграций
- ✅ Выполнена команда `python manage.py migrate`
- ✅ Все таблицы созданы в PostgreSQL

### 7. Создание суперпользователя
- ✅ Создан пользователь `admin` для админ-панели

### 8. Загрузка тестовых данных
- ✅ Загружены данные из `catalogfixture.json`

## Текущие настройки базы данных:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "jango_hw_project",
        "USER": "django_user",
        "PASSWORD": "django123",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Проверка работы:

1. Запустите сервер: `python manage.py runserver`
2. Откройте браузер и перейдите на `http://127.0.0.1:8000/`
3. Проверьте админ-панель: `http://127.0.0.1:8000/admin/`

## Важные замечания:

- Проект полностью переведен на PostgreSQL
- Все данные успешно мигрированы
- Старые файлы SQLite удалены
- Создан новый пользователь базы данных для безопасности

## Команды для управления:

- `python manage.py makemigrations` - создание новых миграций
- `python manage.py migrate` - применение миграций
- `python manage.py createsuperuser` - создание суперпользователя
- `python manage.py loaddata <fixture>` - загрузка данных
- `python manage.py dumpdata` - экспорт данных
