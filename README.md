# Referral System

Простая реферальная система с авторизацией по номеру телефона.

### 📌 Возможности:
- Авторизация по номеру (имитация кода)
- Сохранение инвайт-кода
- Ввод чужого инвайт-кода (один раз)
- Профиль с рефералами
- HTML-интерфейс (Django Templates)
- Документация: Swagger и ReDoc
- Поддержка деплоя на PythonAnywhere (SQLite)

---

### 📌 Запуск
```bash
# Установка проекта
git clone https://github.com/ribondareva/referral-system.git
cd referral-system

# Создание и активация виртуального окружения
python -m venv venv
venv\Scripts\activate         # Windows

# Установка зависимостей
pip install -r requirements.txt

# Создание БД и запуск
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
---

### 📌 Postman
В проекте есть готовая коллекция для ручного тестирования API:
- referral-api.postman_collection.json (в корне проекта)
Импортируйте файл в Postman и используйте готовые запросы.

---
## Доступные маршруты 
```
https://mariabondareva.pythonanywhere.com/
```
Добавьте в строку поиска следующие маршруты:
---
### 📬 API-интерфейс

| Метод | URL                | Назначение                        |
|-------|--------------------|-----------------------------------|
| POST  | `/api/send-code/`  | Отправка кода по номеру           |
| POST  | `/api/verify-code/`| Подтверждение кода и логин        |
| GET   | `/api/profile/`    | Получение профиля пользователя    |
| POST  | `/api/profile/`    | Ввод инвайт-кода                  |

### 📬 Web-интерфейс 

| URL        | Описание                                                |
|------------|---------------------------------------------------------|
| `/login/`  | Страница ввода номера телефона                          |
| `/verify/` | Страница подтверждения кода                             |
| `/profile/`| Профиль пользователя с инвайт-кодом и списком рефералов |

### 📬 API
- Swagger: https://mariabondareva.pythonanywhere.com/swagger/
- ReDoc: https://mariabondareva.pythonanywhere.com/redoc/