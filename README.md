# Admitad Task Project

API:
- create (register, confirm, verify) a user;
- update/get user information (profile);
- create a notification;
- update the notification;
- get a list of all notifications;
- get a list of actual notifications (not yet completed) ones owned by the user;
- get a list of actual notifications (not yet completed) ones where the user is a participant;


Project contains containers:
- nginx
- api-service(DRF)
- postgres
- redis
- celery
- flower (http://0.0.0.0:8001)

##### To speed up the time of the code and api-service using ORJSONParser, Cache(Redis), Nginx, gunicorn
##### For secure part using JWT, filters, permissions.
##### GitHub flow: project with issues(https://github.com/users/sergei-vydra/projects/2)

To launch project:
```docker compose -f docker-compose.yml up -d```

To interact with API via swagger, open in browser:
```http://0.0.0.0/swagger```

To load fixtures use (in 'api' container):
```python manage.py loaddata config/fixture.json```

AdmitadTask project has 2 routers:

- users
- notifications

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

**'notifications'** router. To execute mailing using celery-beat by scheduler.
Possible to create notification and mark as DONE via PATCH method.

**'notifications'** endpoints:
- /api/v1/notifications/
  - **POST**
  - **GET**
- /api/v1/notifications/{id}/
  - **PUT**
  - **PATCH**
  - **GET**
  - **DELETE**
- /api/v1/notifications/consist
  - **GET**
- /api/v1/notifications/own
  - **GET**