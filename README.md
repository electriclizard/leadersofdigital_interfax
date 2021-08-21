# leadersofdigital_interfax


## Требования:
Python >= 3.6
Установленный Docker

### Подготовка
Для Запуска на cpu:
- Необходимо загрузить и разархивировать модели в папку `model_files/`
- сделать pull подготовленного image из DockerHub

## Команды для запуска проекта с помощью Docker:
Загрузите модели командой:
```sh load_models.sh```

Стянем образ
```docker pull electriclizard/leadersofdigital:latest```

Загруженные модели мы передадим в контейнер с помощью Volumes, также прокинем нужный порт и запустим наш image
```docker run -v $PWD/leadersofdigital_interfax/model_files:/usr/src/app/model_files -p 8050:8050 electriclizard/leadersofdigital```

Для запуска без Docker

создайте virtualenv

активируйте virtualenv

```python app.py```

## Вы можете попробовать нашу модель в Colab!

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11_pCGa3fbgoGIKCq2LfzBOWiE4BfcRHX?usp=sharing)

