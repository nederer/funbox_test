# funbox_test Недерер Дмитрий
В качестве формата хранения данных был выбран Sets, все описано в файле Tests.
Тесты Api через Postman.
По умолчанию сервер подключается к RedisDB запущенной на localhost:6379.
Если у Вас другие настройки Redis, то измените переменные REDIS_HOST и REDIS_PORT в файле funbox_testapp.settings.py

Для работы веб приложения необходимо наличие библиотек django, djangorestframework, redis.
Для запуска перейдите в расположение проекта и введите в консоли python manage.py runserver.
