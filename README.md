Инструкция по запуску
```
git clone https://github.com/Splashqq/django-stripe-test-task.git
cd django-stripe-test-task
```
После этого нужно установить переменные окружения внутри проекта в файле .env (в файле .env.example приведен пример переменных)

Запуск с помощью Docker'а
```
docker-compose up -d --build
```

Для корректной работы приложения необходимо:
* создать суперпользователя
```
python manage.py createsuperuser
```
* создать items и order.

* Основные эндпоинты
/item/<id>/ - страница товара с кнопкой оплаты
/buy/<id>/ - API для оплаты товара
/order/<id>/ - страница заказа с кнопкой оплаты
/order/<id>/buy/ - API для оплаты заказа