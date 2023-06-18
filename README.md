## Описание:
```
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
```
## Технологии
**Python 3.9.6**
**Django 3.2**
**djangorestframework 3.12.4**
**djangorestframework-simplejwt 4.7.2**
**PyJWT 2.1.0**
**pytest 6.2.4**
**pytest-django 4.4.0**
**pytest-pythonpath 0.7.3**
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
## Алгоритм регистрации пользователей
**1**.Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
**2**YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
**3**Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
**4**При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).
## Пользовательские роли
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
**Аутентифицированный пользователь (user)** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
**Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
**Суперюзер Django** — обладет правами администратора (admin)
## Функционал проекта по следующим эндпойнтам:
```
В проекте доступны следующие эндпоинты:
```
http://127.0.0.1:8000/api/v1/auth/signup/ POST-запрос — получение кода подтверждения (confirmation_code) на указанный email.
```
```
http://127.0.0.1:8000/api/v1/auth/token/ POST-запрос — получение Access-токена в обмен на username и confirmation_code.
```
```
http://127.0.0.1:8000/api/v1/users/ Доступно для пользователей с ролью "администратор". GET-запрос — получение списка всех пользователей, POST-запрос — добавление нового пользователя.
```
```
http://127.0.0.1:8000/api/v1/users/{username}/ Доступно для пользователей с ролью "администратор". GET-запрос — получение пользователя по username. PATCH-запрос — редактирование данных пользователя. DELETE-запрос — удаление пользователя.
```
```
http://127.0.0.1:8000/api/v1/users/me/ Права доступа — любой зарегистрированный пользователь. GET-запрос — получение данных о своей учётной записи. PATCH-запрос — редактирование своей учётной записи. Изменить роль пользователя нельзя.
```
```
http://127.0.0.1:8000/api/v1/categories/ GET-запрос — получение списка всех категорий (доступно без токена). POST-запрос — создание новой категории (доступно для администратора).
```
```
http://127.0.0.1:8000/api/v1/categories/{slug}/ Доступно для пользователей с ролью "администратор". DELETE-запрос — удаление категории по её slug.
```
```
http://127.0.0.1:8000/api/v1/genres/ GET-запрос — получение списка всех жанров (доступно без токена). POST-запрос — добавление нового жанра (доступно для администратора).
```
```
http://127.0.0.1:8000/api/v1/genres/{slug}/ Доступно для пользователей с ролью "администратор". DELETE-запрос — удаление жанра по его slug.
```
```
http://127.0.0.1:8000/api/v1/titles/ GET-запрос — получение списка всех произведений (доступно без токена). POST-запрос — добавление нового произведения (доступно для администратора).
```
```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/ GET-запрос — получение информации о произведении (доступно без токена). PATCH-запрос — обновление информации о произведении (доступно для администратора). DELETE-запрос — удаление произведения (доступно для администратора).
```
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ GET-запрос — получение списка всех отзывов (доступно без токена). POST-запрос — добавление нового отзыва (доступно для аутентифицированных пользователей). Пользователь может оставить один отзыв на произведение.
```
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/ GET-запрос — получение отзыва о произведении по его id (доступно без токена). PATCH-запрос — изменение отзыва (доступно для администратора, модератора и автора отзыва). DELETE-запрос — удаление отзыва по id (доступно для модератора, администратора и автора отзыва).
```
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ GET-запрос — получение списка комментариев к отзыву (доступно без токена). POST-запрос — добавление комментария к отзыву (доступно для аутентифицированных пользователей).
```
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ GET-запрос — получение информации о комментарии по id (доступно без токена). PATCH-запрос — частичное обновление комментария (доступно для администратора, модератора и автора комментария). DELETE-запрос — удаление комментария (доступно для администратора, модератора и автора комментария).
```
```

## Авторы проекта:
- [Vyacheslav Tarasov](https://github.com/vyacheslavtarasov)
- [Dmitry Pavlenko](https://github.com/DPavlen)
- [Chigina Ekaterina](https://github.com/ekaterinachigina)

