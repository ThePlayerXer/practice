Перед началом работы нужно установить все необходимые расширения
 Расширения:
1. Python
2. Pylance
3. Django
4. Black formatter

Создаем виртуальное окружение
python -m venv venv

Активируем виртуальное окружение
venv\Scripts\activate

Устанавливаем Django и зависимости
pip install django pillow psycopg2-binary django-crispy-forms crispy-bootstrap5 django-filter

Запуск сервера
python manage.py runserver
