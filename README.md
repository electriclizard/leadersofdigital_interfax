# leadersofdigital_interfax


## Требования:
Python >= 3.6
## Команды для запуска проекта:
### Подготовка
Необходимо загрузить и разархивировать модели в папку `model_files/`

Для этого выполните команду
```sh load_models.sh```

Далее соберем образ и установим все зависимоти
```docker build . interfax```

Загруженные модели мы передадим в контейнер с помощью Volumes, также проеинем нужный порт

```docker run -v /Users/cheena/PycharmProjects/leadersofdigital_interfax/model_files:/usr/src/app/model_files -p 8050:8050 interfax```


 Создайте виртуальное окружение:
``` virtualenv venv```  
Активируйте:
``` source venv/bin/activate ``` или ``` venv/Scripts/activate ```  
Установите зависимости: ``` pip install -r requirements.txt```  
Запустите проект ``` python app.py ```
