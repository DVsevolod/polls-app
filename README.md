**Backend сервер для приложения с опросами.**

**Задача:**

Спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:


- [GET] /login/ - авторизация в системе
- [ALL] /polls/ - добавление/изменение/удаление опросов. 
- [ALL] /questions/ - добавление/изменение/удаление вопросов в опросе. 

Функционал для пользователей системы:

- [GET] /active-polls/ - получение списка активных опросов
- [PUT] /active-polls/<pk>/ - прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- [GET] /users/<pk>/ - получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Документация написана при помощи SwaggerUI и доступна по url 

    /swagger/.

Деплой:

Проект залит на Docker Hub, устанавливается при помощи команды:

    docker pull vdanilintest/polls-app

Запуск:

    docker run --rm --name polls -p 8080:8080 vdanilintest/polls-app
    
Остановка:

    docker stop polls

**Swagger (url: /swagger/).**

Для теста необходимо передать в Swagger csrf-токен, возвращенный в headers после авторизации (Postman etc.).

Для упрощения проверки функциональности можно использовать готовые профили.

**Superuser**

    username: admin
    password: admin
    
**User**

    username: qwerty
    password: 12345678
    
**Схема SwaggerUI**

Авторизация:

[login]!(https://github.com/DVsevolod/polls-app/blob/main/img/login.png)

Активные опросы:

[active-polls]!(https://github.com/DVsevolod/polls-app/blob/main/img/active-polls.png)

Пользователи:

[users]!(https://github.com/DVsevolod/polls-app/blob/main/img/users.png)

Опросы:

[polls]!(https://github.com/DVsevolod/polls-app/blob/main/img/polls.png)

Вопросы:

[questions]!(https://github.com/DVsevolod/polls-app/blob/main/img/questions.png)

