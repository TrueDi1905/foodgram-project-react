# Foodgram

http://178.154.199.83/ -Foodgram

### Описание
«Продуктовый помощник» (Проект Яндекс.Практикум) Сайт для публикации кулинарных рецептов. Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в txt формате. 

### Установка
Проект собран в Docker и содержит четыре образа:

1. backend - образ бэка проекта
2. frontend - образ фронта проекта
3. postgres - образ базы данных PostgreSQL
4. nginx - образ web сервера nginx


#### Запуск проекта:
- Установите Docker
- Выполнить команду docker pull truedi1905/foodgram

#### Первоначальная настройка Django:
- docker-compose exec web python manage.py migrate --noinput
- docker-compose exec web python manage.py collectstatic --no-input 

#### Загрузка тестовой фикстуры в базу:
docker-compose exec backend python manage.py loaddata fixtures.json

#### Создание суперпользователя:
- docker-compose exec backend python manage.py createsuperuser
- можно протестировать админку:
login - TrueDi1905
password - dima1212

