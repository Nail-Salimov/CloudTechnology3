
## Салимов Наиль 11-802


Ссылка на Задание 1: https://github.com/Nail-Salimov/CloudTechnology

Ссылка на Задание 2: https://github.com/Nail-Salimov/CloudTechnology2

### Задание 3


#### Info

В этом задании используются две облачные функции и их зависимости, находящиеся в папках ask-function и tgbot-function. Также используется дполонительный Object Storage, где хранятся записи имен и id сообщений.


#### Подготовка дополнительного Object Storage

Параметры:
 - Доступ на чтение объектов: Публичный
 - Доступ к списку объектов: Публичный
 - Доступ на чтение настроек: Ограниченный. 
 - Класс хранилища: Стандартный

В него добавить два пустых файла:
 - message.txt
 - name.txt


#### Облачная функция (в папке ask-function)

Создать триггер для Message Queue, созданную в предыдущем задании на эту функцию.
Настройки дефолтные.
Точка входа: index.handler .
Функция публичная.

Данная функция предназначена для отправки сообщения с фотографией и сообщением: "Кто это?". Также идет запись данных в файл message.txt в формате: {tg_message_id : object_id}  


Для работы, нужно добавить следующие переменные окружения:
	
 - S3_SECRET_KEY   (секретный ключ от аккаунта Yandex Cloud, где находится Object Storage с фотографиями)
 - S3_ACCESS_KEY   (ключ доступа от аккаунта Yandex Cloud, где находится Object Storage  фотографиями)
 - DB_SECRET_KEY   (секретный ключ от аккаунта Yandex Cloud, где находится Object Storage с файлом message.txt)
 - DB_ACCESS_KEY   (ключ доступа от аккаунта Yandex Cloud, где находится Object Storage  файлом message.txt)
 - TG_TOKEN (токен telegram бота)
 - DB_BUCKET (название Object Storage, где находится файл message.txt)
 - CHAT_ID (id чата ботом)
 - DB_OBJECT (object_id файла message.txt)


Также добавить в облачную функцию файл: requirements.txt . 


#### Облачная функция (в папке tgbot-function)

Для этой функции добавить telegram Webhook для этого бота на эту облачную функцию. 

Точка входа: index.handler .
Функция публичная.

Данная функцию предназначена для получению ответов на вопросов: "Кто это?" и запросов фотографий по имени от пользователя боту. Идет запись имен в файл name.txt в формате: {name : [object_id] }

Для работы, нужно добавить следующие переменные окружения:
 - S3_SECRET_KEY   (секретный ключ от аккаунта Yandex Cloud, где находится Object Storage с фотографиями)
 - S3_ACCESS_KEY   (ключ доступа от аккаунта Yandex Cloud, где находится Object Storage  фотографиями)
 - DB_SECRET_KEY   (секретный ключ от аккаунта Yandex Cloud, где находится Object Storage с файлом message.txt и name.txt)
 - DB_ACCESS_KEY   (ключ доступа от аккаунта Yandex Cloud, где находится Object Storage  файлом message.txt и name.txt)
 - TG_TOKEN (токен telegram бота)
 - DB_BUCKET (название Object Storage, где находится файл message.txt)
 - CHAT_ID (id чата ботом)
 - DB_MESSAGE_OBJECT (object_id файла message.txt)
 - DB_NAME_OBJECT (object_id файла name.txt)
 - IMAGES_BUCKET_ID (название Object Storage, где находятся фотографии)

Также добавить в облачную функцию файл: requirements.txt .

#### Пользование ботом

Функции:
 - ответ на вопрос: Кто это? через Ответить
 - поиск по имени: /find ИМЯ 