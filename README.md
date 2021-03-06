# leadersofdigital_interfax


## Требования:
Python >= 3.6
Установленный Docker

### Подготовка
Загрузка весов моделей

Вариант 1 - автоматизированный:
- Необходимо загрузить и разархивировать модели в папку `model_files/`
- Для этого нужно создать virtualenv с python3 и установить библиотеку gdown

- `python3 -m venv venv/`
- `source venv/bin/activate`
- `pip install gdown`
- Загрузите модели командой:
  ```sh load_models.sh```

Вариант 2:
- загрузить руками [Архив с весами модели](https://drive.google.com/file/d/16iOzmpngF-t7b_wzeU3bxcQ8mB1QpWzD/view?usp=sharing)
- извлечь содержимое архива в папку `model_files/`

Для Запуска на cpu:
- сделать pull подготовленного image из DockerHub

#### Для запуска без Docker

- активируйте virtualenv

- установите все зависимости `pip install -r requirements.txt`

- запустите сервис ```python app.py```

#### Для запуска без Docker на GPU:
- заменить в `configs/models.py` в классе `BertConfig` значение в строке 7 на `device: str = 'cuda'`
- запустите сервис ```python app.py```

## Команды для запуска проекта с помощью Docker:

Стянем образ
```docker pull electriclizard/leadersofdigital:latest```

Загруженные модели мы передадим в контейнер с помощью Volumes, также прокинем нужный порт и запустим наш image
```docker run -v ${PWD}/model_files:/usr/src/app/model_files -p 8050:8050 electriclizard/leadersofdigital```

#### Для запуска с Docker на GPU необходимо:
- установленный nvidia docker
- установленный nvidia-driver
- заменить в `configs/models.py` в классе `BertConfig` значение в строке 7 на `device: str = 'cuda'`
- тогда команда запуска контейнера будет вглядеть так: 
`docker run --gpus all -v ${PWD}/model_files:/usr/src/app/model_files -p 8050:8050 electriclizard/leadersofdigital`

## Вы можете попробовать нашу модель в Colab!

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11_pCGa3fbgoGIKCq2LfzBOWiE4BfcRHX?usp=sharing)

