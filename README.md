# Проект интернет-магазин MEGANO

MEGANO - интернет-магазин для покупки различных товаров. На главной странице отображается банер, 
популярные продукты, лимитированное издание. Присутствует вкладка товаров со скидками. Самое основное -
это коталог с функцией поиска, фильтрами, сортировкой. В сервисе доступна админка для управления товарами.

####
# ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi)

<div align="middle">
   <img src="https://s11.gifyu.com/images/SO3PA.png" width="60%"></img>
</div>


## Установка

1. Клонируйте или скачайте репозиторий с gitlab/github
2. Выполните команду `python manage.py migrate` из папки с проектом
3. Введите команду `python manage.py runserver` из папки с проектом


## Демонстрация

Для просмотра функционала megano:

1) Разархивируйте uploads в проект.
2) Установите фикстуры выполнив команду из папки с проектом `python manage.py loaddata megano-fixtures.json`

*Пользователи созданные для демонстрации*

1) Админ
   - Роль - Admin
   - Логин - admin
   - Пароль - admin
2) Пользователь
   - Роль - User
   - Логин - John
   - Пароль - 123456
