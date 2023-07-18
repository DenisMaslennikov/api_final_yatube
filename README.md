# API Yatube
## Апи для работы с блогами "Yatube":
* Можно читать публикации пользователей
* Можно добавлять/редактировать свои публикации
* Зарегистрированные пользователи могут оставлять комментарии к постам других пользователей.
* Есть возможность редактировать собственные комментарии
* Есть механизм сообществ. Используя апи можно получить список сообществ или информацию о конкретном сообществе
* Зарегистрированные пользователи могут подписываться друг на друга.

Использование данного апи позволит вам реализовать свои собственные приложения для работы с популярной платформой блогов Yatube.

## Локальная установка:
1. Скачиваем проект с гитхаба
```commandline
git clone <ссылка на проект> <директория проекта>
```
2. Создаем виртуальное окружение в директории проекта
```commandline
cd <директория проекта>
python -m venv venv
```
3. Активируем виртуальное окружение
```commandline
source env/bin/activate
```
4. Обновляем pip
```commandline
python -m pip install --upgrade pip
```
5. Устанавливаем пакеты необходимые для проекта
```commandline
pip install -r requirements.txt
```
6. Выполняем миграции
```commandline
cd yatube_api
python manage.py migrate
```
7. Запускаем веб сервер разработки
```commandline
python manage.py runserver
```

## Документация API
Полная версия документации доступна по [ссылке](http://127.0.0.1:8000/redoc/) при запущенном веб сервере разработки

Несколько примеров запросов к API:

* Получение токена авторизации
```http request
POST http://127.0.0.1:8000/api/v1/jwt/create/
{
  "username": "string",
  "password": "string"
}
```
```json
{
  "refresh": "string",
  "access": "string"
}
```
* Обновление токена
```http request
POST http://127.0.0.1:8000/api/v1/jwt/refresh/
{
  "refresh": "string"
}
```
```json
{
  "access": "string"
}
```
* Получение списка публикаций
```http request
GET http://127.0.0.1:8000/api/v1/posts/?limit=<число>&offset=<число>
```
`limit` - Количество публикаций на странице

`offset` - Номер страницы
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
* Создание новой публикации
```http request
POST http://127.0.0.1:8000/api/v1/posts/
Authorization: <Ваш токен>
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
* Обновление публикации: отправьте `PUT` или `PATCH` запрос 
```http request
PUT|PATCH http://127.0.0.1:8000/api/v1/posts/<id>/
Authorization: <Ваш токен>
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
`<id>` - ID публикации которую необходимо обновить
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
* Получение конкретной публикации
```http request
GET http://127.0.0.1:8000/api/v1/posts/<id>/
```
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
* Удаление публикации
```http request
DELETE http://127.0.0.1:8000/api/v1/posts/<id>/
Authorization: <Ваш токен>
```
* Получение списка комментариев
```http request
GET http://127.0.0.1:8000/api/v1/posts/<post_id>/comments/
```
`<post_id>` - ID поста для которого надо получить комментарии
```json
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```
* Создание комментария
```http request
POST http://127.0.0.1:8000/api/v1/posts/<post_id>/comments/
Authorization: <Ваш токен>
{
  "text": "string"
}
```
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```
* Получение конкретного комментария
```http request
GET http://127.0.0.1:8000/api/v1/posts/<post_id>/comments/<comment_id>/
```
`<comment_id>` - ID комментария
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```
*Обновление комментария - `PUT` или `PATCH`запрос:
```http request
PUT|PATCH http://127.0.0.1:8000/api/v1/posts/<post_id>/comments/<comment_id>/
Authorization: <Ваш токен>
{
  "text": "string"
}
```
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```
* Удаление комментария
```http request
DELETE http://127.0.0.1:8000/api/v1/posts/<post_id>/comments/<comment_id>/
Authorization: <Ваш токен>
```
* Получение списка сообществ
```http request
GET http://127.0.0.1:8000/api/v1/groups/
```
```json
[
  {
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
  }
]
```
* Получение информации о конкретном сообществе
```http request
GET http://127.0.0.1:8000/api/v1/groups/<group_id>/
```
```json
{
  "id": 0,
  "title": "string",
  "slug": "string",
  "description": "string"
}
```
* Получение списка своих подписок
```http request
GET http://127.0.0.1:8000/api/v1/follow/
Authorization: <Ваш токен>
```
```json
[
  {
    "user": "string",
    "following": "string"
  }
]
```
* Подписка на пользователя
```http request
POST http://127.0.0.1:8000/api/v1/follow/
Authorization: <Ваш токен>
{
  "following": "username"
}
```
```json
{
  "user": "string",
  "following": "string"
}
```