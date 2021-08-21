# leadersofdigital_interfax


## Требования:
Установленный Docker

### Подготовка
Для Запуска на cpu:
- Необходимо загрузить и разархивировать модели в папку `model_files/`
- сделфть pull подготовленного image из DockerHub

## Команды для запуска проекта:
Загрузите модели командой:
```sh load_models.sh```

Стянем образ
```docker pull electriclizard/leadersofdigital:latest```

Загруженные модели мы передадим в контейнер с помощью Volumes, также прокинем нужный порт и запустим наш image
```docker run -v $PWDleadersofdigital_interfax/model_files:/usr/src/app/model_files -p 8050:8050 electriclizard/leadersofdigital```