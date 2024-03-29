# Admitad Task Project

API:
- create (register, confirm, verify) a user;
- update/get user information (profile);
- create a reminder;
- update the reminder;
- get a list of all reminders;
- get a list of actual reminders (not yet completed) ones owned by the user;
- get a list of actual reminders (not yet completed) ones where the user is a participant;


Project contains containers:
- nginx
- api-service(DRF) + admin panel (http://0.0.0.0/admin)
- postgres
- redis
- celery
- flower (http://0.0.0.0:8001)

##### To speed up the time of the code and api-service using ORJSONParser, Cache(Redis), Nginx, gunicorn
##### For secure part using JWT, filters, permissions.
##### To monitoring errors using Sentry service.
##### GitHub flow: project with issues(https://github.com/users/sergei-vydra/projects/2)

To launch project:
- use **main** branch of git project:
```https://github.com/sergei-vydra/admitad-task.git```
- than
```docker compose -f docker-compose.yml up -d```

To interact with API via swagger, open in browser:
```http://0.0.0.0/swagger```

To run tests (in 'api' container):
```python manage.py test``` or via task ```task t```

To load fixtures use (in 'api' container):
```python manage.py loaddata config/data/fixture.json``` or via task ```task ld```

AdmitadTask project has 2 routers:

- users
- reminders

**'users'** router uses 'dj-rest-auth' lib. Using the lib helps me develop mostly all users endpoint quickly. But it has
some issues:

- I fixed some of the endpoints (verify-email, logout, password-reset), because they had a bugs
- in background the lib sends email via python code(synchronously)

**'users'** endpoints:
- /api/v1/users/login/
    - **POST**
- /api/v1/users/logout/
    - **POST**
- /api/v1/users/password/change/
    - **POST**
- /api/v1/users/password/reset/
    - **POST**
- /api/v1/users/password/reset/confirm/
    - **POST**
- /api/v1/users/password/reset/confirm/{uidb64}/{token}/
    - **POST**
- /api/v1/users/registration/
    - **POST**
- /api/v1/users/registration/account-confirm-email/{key}/
    - **POST**
    - **GET** (using)
- /api/v1/users/registration/resend-email/
    - **POST**
- /api/v1/users/registration/verify-email/
    - **POST**
- /api/v1/users/token/refresh/
    - **POST**
- /api/v1/users/token/verify/
    - **POST**
- /api/v1/users/user/
    - **PUT**
    - **PATCH**
    - **GET**
- /api/v1/users/
    - **GET**

**'reminders'** router. To execute mailing using celery-beat by scheduler.
Possible to create reminder and mark as DONE via PATCH method.

**'reminders'** endpoints:
- /api/v1/reminders/
  - **POST**
  - **GET**
- /api/v1/reminders/{id}/
  - **PUT**
  - **PATCH**
  - **GET**
  - **DELETE**
- /api/v1/reminders/consist
  - **GET**
- /api/v1/reminders/own
  - **GET**

## Next project steps:
- Rewrite user creating to send email via celery
- Add more endpoints (most used) to cache
- Write more tests
- Fix code (add validators etc.)

### Issues after review:
+ есть докеригнор
+ есть пипенв
+ дока
+ swagger
+ сеттинги разбиты по файлам
+ parameterized в тестах
+ есть лимиты на таски селери
+ хорошее покрытие
Докеризирован проект
Не сделано одним комито
использовал ветки
хорошее редми
хелз чек для бд (скорее всего унесен с другого проекта)
Прибиты гвоздями версии либ
Прибиты гвоздями версии инфры
Vitalii Fedorov
2:20 PM
- Нету ретраев на таски селери
- Нет сервисного слоя, размаз бизнес-логики между сериализаторами, тасками, utils.py
- Нет аннотаций типов, нет mypy
- Cеттинги от всего проекта в api, а не в корне
- Вьюхи не в api, не понятно по какому принзнаку создан модуль api, инфраструктура есть и там и в app, общие утилиты тоже есть в обоих модулях
- Не использовал билд-образ в докере
- Тестирование бизнес-логики через вьюхи и таски, базовый тест кейс для всех тест кейсов, даже для тестов тасок, унаследован
Vitalii Fedorov
2:30 PM
декомпозиция проекта плохая
тайпинг только в енвах
енвы постгры в открытом виде в докер компосе и дублирование енвов проекта
логлевел в селери инфо 
в селери в депенс апи? зачем
Все живет в селери бит что плохо так как у нас таски могут начать отставать из за долгой логки
Скрипт с гуникорном но с мейкмигратионс и миграцией
оба игнора избыточный 
два конфига nginx зачем?
огромная фикстура всей бд в том числе с приватными данными
Vitalii Fedorov
2:35 PM
код сломается в продакшене, как только там появится весомое количество пользоваталей, будет заблокирована транзакцией вся база, нотификации не будут доставлены вовремя. Мейлы не будут доставлены при сетевых сбоях. При сбое одной отправки мейла будет попытка отката всей транзакции, хотя в этой же транзакции предыдущие мейлы уже были высланы. Нету сервисного слоя и нету аннотаций типов, что является критичным в плане читаемости и работы в команде. Человек запарился с технологиями, и показал что зн
Мейлы не будут доставлены при сетевых сбоях. При сбое одной отправки мейла будет попытка отката всей транзакции, хотя в этой же транзакции предыдущие мейлы уже были высланы. Нету сервисного слоя и нету аннотаций типов, что является критичным в плане читаемости и работы в команде. Человек запарился с технологиями, и показал что знает фреймворк, но забыл про бизнес-задачу.
