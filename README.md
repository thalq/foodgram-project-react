![foodgram-project-react](https://github.com/thalq/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Foodgram - «Продуктовый помощник»

## Описание проекта
> Пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд
----

### :bust_in_silhouette: Пользователи
**Список пользователей.**
- _`GET` http://158.160.4.74/api/users/_
<br />


**Регистрация пользователя.**
- _`POST` http://158.160.4.74/api/users/_
<br />


**Профиль пользователя.**
- _`GET` http://158.160.4.74/api/users/{id}/_
<br />


**Текущий пользователь.**
- _`GET` http://158.160.4.74/api/users/me/_
<br />

**Изменение пароля.**
- _`POST` http://158.160.4.74/api/users/set_password/_
<br />

**Получить токен авторизации.**
- _`POST` http://158.160.4.74/api/auth/token/login/_
<br />

**Удаление токена.**
- _`POST` http://158.160.4.74/api/auth/token/logout/_
<br />

----

### :pushpin: Теги

**Cписок тегов**
- _`GET` http://158.160.4.74/api/tags/_
<br />


**Получение тега**
- _`GET` http://158.160.4.74/api/tags/{id}/_
<br />

----

### :fork_and_knife: Рецепты

**Список рецептов**
- _`GET` http://158.160.4.74/api/recipes/_
<br />

**Создание рецепта**
- _`POST` http://158.160.4.74/api/recipes/_
<br />

**Получение рецепта**
- _`GET` http://158.160.4.74/api/recipes/{id}/_
<br />

**Обновление рецепта**
- _`PATCH` http://158.160.4.74/api/recipes/{id}/_
<br />


**Удаление рецепта**
- _`DEL` http://158.160.4.74/api/recipes/{id}/_
<br />

----

### :memo: Список покупок

**Скачать список покупок**
- _`GET` http://158.160.4.74/api/recipes/download_shopping_cart/_
<br />

**Добавить рецепт в список покупок**
- _`POST` http://158.160.4.74/api/recipes/{id}/shopping_cart/_
<br />

**Удалить рецепт из списка покупок**
- _`DEL` http://158.160.4.74/api/recipes/{id}/shopping_cart/_
<br />

----

### :star2: Избранное

**Добавить рецепт в избранное**
- _`POST` http://158.160.4.74/api/recipes/{id}/favorite/_
<br />

**Удалить рецепт из избранного**
- _`DEL` http://158.160.4.74/api/recipes/{id}/favorite/_
<br />

----

### :+1: Подписки

**Мои подписки**
- _`GET` http://158.160.4.74/api/users/subscriptions/_
<br />

**Подписаться на пользователя**
- _`POST` http://158.160.4.74/api/users/{id}/subscribe/_
<br />

**Отписаться от пользователя**
- _`DEL` http://158.160.4.74/api/users/{id}/subscribe/_
<br />

----

### :tomato: Ингредиенты

**Список ингредиентов**
- _`GET` http://158.160.4.74/api/users/ingredients/_
<br />

**Получение ингредиента**
- _`GET` http://158.160.4.74/api/users/ingredients/{id}/_
<br />

----

## :wrench: Установка
Клонируем репозиторий:

```$ git clone git@github.com:thalq/foodgram-project-react.git```

Подключаемся к серверу через ssh и перейдите в каталог
/home/< username >/foodgram/

Запускаем установку и сборку контейнеров
docker compose up -d

----
# Автор проекта
Таня Халквист
