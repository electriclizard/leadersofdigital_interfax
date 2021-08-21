# leadersofdigital_interfax


## Требования:
Docker

### Подготовка
Необходимо загрузить и разархивировать модели в папку `model_files/`

## Команды для запуска проекта:
Для этого выполните команду
```sh load_models.sh```

Далее соберем образ и установим все зависимоти
```docker build . -t interfax```

Загруженные модели мы передадим в контейнер с помощью Volumes, также прокинем нужный порт

```docker run -v /Users/cheena/PycharmProjects/leadersofdigital_interfax/model_files:/usr/src/app/model_files -p 8050:8050 interfax```
