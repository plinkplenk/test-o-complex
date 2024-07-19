# [test-complex-o](https://weather.yoky.site/)

## Приложение, которое показывает погоду.
### Было сделано:

- Автодополнение поиска;
- Приложение запоминает какой город вы смотрели в последний раз и сразу показывает этот город;
- Есть возможно запустить приложение в Docker.


### Для создания приложение использовались:

- Python v3.12.2
- Django 5.0
- TailwindCSS
- JavaScript/HTML


### Для запуска приложение:
1. переименовать example.env -> .env
    ```bash
    mv example.env .env
    ```

2. Зарегистрироваться на https://www.weatherapi.com/ , получить API KEY, затем добавить его в .env
3. запустить приложение с помощью Docker
    ```bash
    docker build . --tag weather && docker run --env-file .env -p 8000:8000 -d weather:latest
    ```
