
# API для Yamdb

## Описание

API для проекта Yamdb

## Технологии

```
Python 3.9
Django 3.2
REST API Framework
```

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:NikolayPetrow23/api_yamdb.git

cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv

python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Авторы

```
Николай Петров - управление пользователями (Auth и Users)
Александр Сакулин - категории (Categories), жанры (Genres) и произведения (Titles)
Артем Чулошников - отзывы (Review) и комментарии (Comments)
```
