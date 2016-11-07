## DjangoBase

Набор базовых компонентов, для разработки типовых веб-проектов на основе фреймворка Django.
Цель данного проекта - иметь под рукой программное решение для быстрого развертывания и последущей доработки типового web-проекта на основе стека Python/Django, с минимальным количеством зависимостей.

### Данная версия включает в себя следующие приложения (модули)

* accounts - модуль для работы с учетными записями пользователей
* gallery - модуль для работы с галереями изображений
* pages - модуль для работы с контентными страницами
* news - модуль для работы с новостными страницами и лентой новостей

### Используемое программное обеспечение

Серверная часть:
* Pillow==4.2.1
* Django==1.11.3
* django-mptt==0.8.7
* django-ckeditor==5.3.0

Клиентская часть:
* JQuery v3.2.1
* Bootstrap v3.5.7


## Использование

### Первый способ (классический)
Создайте каталог, в которм предполагается развернуть проект:
```shell
$ mkdir ~/my_project_venv
```
Создайте виртуальное окружение Python3 в данном каталоге и перейдите в него:
```shell
$ virtualenv --python=$(which python3) ~/my_project_venv && cd ~/my_project_venv
```
Активируйте виртуальное окружение Python:
```shell
$ source ./bin/activate
```
Склонируйте данный git-репозиторий и перейдите в каталог приложения:
```shell
$ git clone https://github.com/ChaoticEvil/django_base.git && cd django_base
```
Установите необходимые python-пакеты:
```shell
$ pip install -r reqs.list
```
Создайте таблицы в базе данных (по-умолчанию используется sqlite3), примените файлы миграций и создайте привилегированного пользователя:
```shell
$ python manage.py migrate && python manage.py syncdb
```
Запустите веб-сервер приложения:
```shell
$ python manage.py runserver
```

### Второй способ (автоматический)
Склонируйте данный git-репозиторий себе на компьютер и перейдите в каталог проекта:
```shell
$ git clone https://github.com/ChaoticEvil/django_base.git && cd django_base
```
Выполните скрипт автоматической развертки и далее следуйте инструкциям:
```shell
bin/deploy.sh [NEW_PROJECT_NAME] [NEW_PROJECT_ROOT_DIR]
```
Например:
```shell
$ sh bin/new_project.sh my_super_mega_project ~/
```
или
```shell
$ sh bin/new_project.sh mega_cool_project /var/www/
```

### Пересоздание таблиц в БД
Для очистки текущих данных и пересоздания таблиц БД выполните:
```shell
$ sh bin/deploy.sh
```
