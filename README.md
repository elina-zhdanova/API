# URL Shortener Service

## Описание проекта
Сервис для сокращения длинных URL-адресов с возможностью:
- Генерации коротких ссылок
- Просмотра статистики переходов
- Управления ссылками (деактивация)
- Автоматического истечения срока действия ссылок

## Технологии
- Python 3.9+
- Flask
- SQLAlchemy (MySQL)
- Marshmallow (валидация данных)
- Flask-HTTPAuth (аутентификация)
- Flask-ApiSpec (документация API)

## Установка и запуск
### 1. Предварительные требования
- Установленный Python 3.9+
- MySQL сервер
- Установленный 'pip'

### 2. Настройка окружения
1. Клонируйте репозиторий:
git clone <repository-url>
cd url-shortener

2. Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

3. Установите зависимости:
pip install -r requirements.txt

### 3. Настройка базы данных
1. Создайте базу данных в MySQL:
CREATE DATABASE url_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

2. Настройте подключение в файле `.env`:
DATABASE_URL=mysql+pymysql://username:password@localhost/url_db
SECRET_KEY=your-secret-key-here

### 4. Запуск миграций
flask db init
flask db migrate
flask db upgrade

### 5. Создание администратора
flask create-user admin password123

### 6. Запуск приложения
flask run

Приложение будет доступно по адресу: `http://localhost:5000`

## Использование API

Документация API доступна по адресу: `http://localhost:5000/api/docs`

### Примеры запросов

1. Создание короткой ссылки:
curl -X POST -u admin:password123 \
-H "Content-Type: application/json" \
-d '{"original_url":"https://example.com/very/long/url"}' \
http://localhost:5000/api/v1/shorten

2. Получение списка ссылок:
curl -u admin:password123 http://localhost:5000/api/v1/links

3. Деактивация ссылки:
curl -X PUT -u admin:password123 http://localhost:5000/api/v1/links/1/deactivate

4. Получение статистики:
curl -u admin:password123 http://localhost:5000/api/v1/stats
