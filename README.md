# Foodgram

Сервис, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Функция «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

```
http://84.252.136.244/
Admin account: admin
Password: Foodgram
```

## Шаблон наполнения env-файла
```
infra/.env

DB_ENGINE=
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```

## Как развернуть проект на локальной машине
- Клонируйте репозиторий:
```
git@github.com:kupl0xa/foodgram-project-react.git
```
- Перейдите в папку infra:
```
cd foodgram-project-react/infra
```
- Выполните команду
```
docker-compose up
```