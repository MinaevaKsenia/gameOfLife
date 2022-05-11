# Игра Жизнь

В проекте реализован клиентский сервер игры Жизнь. Для разработки использовался фреймворк Flask.

#### Порядок запуска для локального тестирования:
- Развернуть виртуальное окружение
- Активировать виртуальное окружение /venv/Scripts/activate
- Установить зависимости проекта из файла requirements.txt
- Установить переменную окружения FLASK_APP на main.py
- Установить переменную окружения PYTHONPATH на папку src
- Запустить проект командой: python src\main.py.

#### Доступные маршруты:
#### 1. Авторизация
/login
#### 2. Регистрация
/register
#### 3. Главная страница
/