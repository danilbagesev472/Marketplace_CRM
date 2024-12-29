# 📚 Документация Бэкенда

## 🔍 Обзор Проекта

Этот бэкенд-проект предназначен для управления аутентификацией пользователей и их регистрацией с использованием JWT (JSON Web Tokens). Он включает модули для обработки регистрации пользователей, аутентификации и управления доступом на основе ролей.

## 📑 Содержание

- [🔧 Установка](#-установка)
- [⚙️ Настройка](#️-настройка)
- [📂 Структура Проекта](#-структура-проекта)
- [🚀 Использование](#-использование)
- [🌐 API Эндпоинты](#-api-эндпоинты)

## 🔧 Установка

Для начала работы с бэкендом убедитесь, что у вас установлен Python 3.8+. Затем клонируйте репозиторий и установите необходимые зависимости.

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject/Back
pip install -r requirements.txt
```

## ⚙️ Настройка

Переменные Окружения: Создайте файл .env в корневой директории и добавьте необходимые переменные окружения. Например:

```
DATABASE_URL=ваш_адрес_базы_данных
SECRET_KEY=ваш_секретный_ключ
```

Миграция Базы Данных: Выполните следующую команду для применения миграций базы данных:

```bash
alembic upgrade head
```

## 📂 Структура Проекта

    Back/
    │
    ├── main.py                # Точка входа в приложение
    ├── routes/                # Директория с модулями маршрутов
    │   ├── __init__.py
    │   ├── crm.py
    │   ├── products.py
    │   └── users.py
    ├── models/                # Директория с моделями базы данных
    │   ├── __init__.py
    │   └── user.py
    ├── auth_x_jwt/            # Директория для модуля аутентификации JWT
    │   ├── __init__.py
    │   └── auth.py
    └── utils/                 # Утилиты и вспомогательные функции
    	├── __init__.py
    	└── hashing.py

## 🚀 Использование

Чтобы запустить сервер бэкенда, выполните следующую команду:

```bash
uvicorn main:app --reload
```

Сервер будет запущен на

```bash
http://127.0.0.1:8000/
```

## 🌐 API Эндпоинты

### 📝 Регистрация Пользователя

    Эндпоинт: /register
    Метод: POST
    Описание: Регистрирует нового пользователя.
    Тело Запроса:

    {
    	"name": "Иван Иванов",
    	"email": "ivan.ivanov@example.com",
    	"phone": "1234567890",
    	"password": "securepassword"
    }

### 🔑 Аутентификация Пользователя

    Эндпоинт: /login
    Метод: POST
    Описание: Аутентифицирует пользователя и возвращает JWT токен.
    Тело Запроса:

    {
    	"email": "ivan.ivanov@example.com",
    	"password": "securepassword"
    }
