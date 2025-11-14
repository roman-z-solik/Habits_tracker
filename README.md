# Habits Tracker

Django REST API для трекера полезных привычек по книге "Атомные привычки" Джеймса Клира. Приложение позволяет пользователям создавать, отслеживать и управлять своими привычками с системой напоминаний через Telegram.

## Технологии
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)        
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)  
![DjangoREST](https://img.shields.io/badge/Django%20REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-%2337814A.svg?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

## Использование
Открыть проект в 
![Pycharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)  

### Приложение users

`users/models.py`:

Класс User - кастомная модель пользователя с дополнительным полем telegram_chat_id для интеграции с Telegram-уведомлениями.

`users/serializers.py`:

Класс RegisterSerializer - сериализатор для регистрации пользователей с валидацией паролей  
Класс UserSerializer - сериализатор для отображения профиля пользователя

`users/views.py`:

Класс RegisterView - обработка регистрации новых пользователей  
Класс UserProfileView - получение профиля текущего пользователя

### Приложение habits

`habits/models.py`:

Класс Habit - модель привычки с полями: место, время, действие, признак приятной привычки, связанная привычка, периодичность, вознаграждение, время выполнения и признак публичности. Связана с пользователем отношением один-ко-многим.

`habits/serializers.py`:

Класс HabitSerializer - сериализатор для CRUD операций с привычками  
Класс HabitListSerializer - сериализатор для списка привычек с ограниченным набором полей

`habits/views.py`:

Класс HabitViewSet - ViewSet для полного цикла операций с привычками  
Метод public - кастомное действие для получения списка публичных привычек

`habits/validators.py`:

Функция validate_habit - валидатор привычек согласно правилам книги:  
- Исключает одновременный выбор связанной привычки и вознаграждения  
- Ограничивает время выполнения 120 секундами  
- Проверяет, что в связанные привычки попадают только приятные привычки  
- Запрещает приятным привычкам иметь вознаграждение или связанные привычки

`habits/permissions.py`:
Класс IsOwner - разрешение только для владельца объекта привычки

### Приложение habits (дополнение)

`habits/tasks.py`:

Функция send_telegram_reminder - задача Celery для отправки напоминаний о привычках через Telegram  
Функция check_habits_for_reminders - периодическая задача для проверки привычек, которые нужно выполнить  
Функция send_daily_reminders - ежедневная проверка привычек для напоминаний

## API Endpoints

### Аутентификация

- `POST /api/users/token/` - получение JWT токена
- `POST /api/users/token/refresh/` - обновление JWT токена

### Пользователи

- `POST /api/users/register/` - регистрация нового пользователя
- `GET /api/users/profile/` - получение профиля текущего пользователя

### Привычки (ViewSet)

- `GET /api/habits/habits/` - список привычек текущего пользователя с пагинацией
- `POST /api/habits/habits/` - создание новой привычки
- `GET /api/habits/habits/{id}/` - получение конкретной привычки
- `PUT /api/habits/habits/{id}/` - полное обновление привычки
- `PATCH /api/habits/habits/{id}/` - частичное обновление привычки
- `DELETE /api/habits/habits/{id}/` - удаление привычки
- `GET /api/habits/habits/public/` - список публичных привычек

### Документация

- `GET /swagger/` - интерактивная документация Swagger
- `GET /redoc/` - альтернативная документация ReDoc

## Функциональность

### Валидация привычек
- Реализована полная валидация согласно правилам книги "Атомные привычки"
- Проверка времени выполнения (не более 120 секунд)
- Контроль связанных привычек и вознаграждений
- Валидация периодичности выполнения

### Telegram уведомления
- Интеграция с Telegram Bot API для отправки напоминаний
- Автоматическая проверка привычек по расписанию
- Персонализированные сообщения с деталями привычки

### Пагинация
- Реализована пагинация для списков привычек
- Вывод по 5 привычек на страницу
- Стандартная Django REST Framework пагинация

### Права доступа
- JWT аутентификация для всех защищенных эндпоинтов
- Пользователи имеют доступ только к своим привычкам
- Публичные привычки доступны для просмотра всем аутентифицированным пользователям
- Права доступа IsOwner для операций с привычками

### Отложенные задачи
- Использование Celery для фоновых задач
- Redis как брокер сообщений
- Периодические задачи для проверки привычек
- Асинхронная отправка Telegram-уведомлений

### Тестирование
- Написаны тесты для моделей пользователей и привычек
- Тестирование API эндпоинтов
- Проверка валидации привычек
- Тестирование прав доступа

-----------------------------------
В проекте присутствует файл
### requirements.txt  
Файл с зависимостями pip для проекта. Для установки зависимостей следует в терминале (возможно в терминале PyCharm) ввести команду:
```bash
pip install -r requirements.txt
```

## Настройка окружения
### Создайте файл .env на основе .env.example:
SECRET_KEY              #SECRET_KEY for django project  
DEBUG                   #DEBUG mode on/off (True/False)  
BASE_NAME               #NAME of postgres database  
BASE_USER               #USERNAME for postgres database  
BASE_PASSWORD           #PASSWORD for postgres database  
BASE_HOST               #HOST for postgres database  
BASE_PORT               #PORT for postgres database  
TELEGRAM_BOT_TOKEN      #Your telegram bot token from botfather  
TELEGRAM_ADMIN_CHAT_ID  #Your telegram chat id from userinfobot  

## Запуск приложения
```bash
# Выполнение миграций
python manage.py migrate
```
```bash
# Создание суперпользователя
python manage.py createsuperuser
```

```bash
# Запуск сервера разработки
python manage.py runserver
```

```bash
# Запуск Celery worker (в отдельном терминале)
celery -A config worker -l info
```

```bash
# Запуск Celery beat (в отдельном терминале)
celery -A config beat -l info
```
```bash
Запуск тестов
Для запуска тестов выполните команду:
python manage.py test
```
```bash
#Проверка качества кода
flake8 --exclude=migrations --max-line-length=119
```

## Требования
### Для установки и запуска проекта, необходимы:

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)  
[Python](https://www.python.org/) - интерпретатор Python версии 3.8+

![PyCharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)  
[PyCharm](https://www.jetbrains.com/pycharm/) - среда разработки (рекомендуется)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)  
[Django](https://www.djangoproject.com/) - веб-фреймворк для Python

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)  
[PostgreSQL](https://www.postgresql.org/) - система управления базами данных

![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)  
[Redis](https://redis.io/) - кэш и брокер сообщений для Celery

## Команда проекта
[Roman Z](https://github.com/roman-z-solik)