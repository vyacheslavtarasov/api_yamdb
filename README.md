## Описание:
Проект «api_yamdb». Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
## Технологии
Python 3.10, Django 3.2
## Как запустить
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:yandex-praktikum/api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
## Функционал проекта по следующим эндпойнтам:
```
В проекте доступны следующие эндпоинты:

Пользователь отправляет POST-запрос с параметрами email и username на
http://127.0.0.1:8000/api/v1/auth/signup/ - Получение кода подверждения на email
{ "email": "string", "username": "string" }
Сервис YaMDB отправляет письмо с кодом подтверждения 
(confirmation_code) на указанный адрес email.

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на
http://127.0.0.1:8000/api/v1/auth/token/ - Получение JWT-токена. 
для авторизации { "username": "string", "confirmation_code": "string" }
После регистрации и получения токена пользователь может отправить 
PATCH-запрос на эндпоинт http://127.0.0.1:8000/api/v1/users/me/ и заполнить поля в 
своём профайле (описание полей — в документации).
http://127.0.0.1:8000/api/v1/users/ - Создание пользователя и получение 
информации о всех пользователях. Доступны GET, POST запросы.
```
## Технологии

- [Vyacheslav Tarasov](https://github.com/vyacheslavtarasov)
- [Dmitry Pavlenko](https://github.com/DPavlen)
- [Chigina Ekaterina](https://github.com/ekaterinachigina)
