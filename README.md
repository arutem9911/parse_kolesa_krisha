# Парсинг сайтов колеса и крыша



## Сервис парсинга

Сервис написан для расчета стоимости имущества выставленного на залог.
Данный сервис только собирает данные и записывает данные в бд POSTGRESQL

Парсит объявления сайтов koresa.kz и krisha.kz

## Для запуска проекта


```commandline
cd your_repo
git clone git@github.com:arutem9911/parse_kolesa_krisha.git
```


Создаем виртуальное окружение и устанавливаем зависимости
```commandline
poetry shell
poetry install
```

В корневой папке есть proxies.py
```python
proxies = [
    "Напишите сюда список своих прокси"
]
```

Создаем .env для хранения переменных окружения
```commandline
WWW_SH_HOST = '0.0.0.0'
WWW_SH_PORT = "8080"
WWW_SH_WORKER = "1"
FASTAPI_CONFIG = 'DEV'
MONGO_URI = "Вставить строку подключения к MONGO_DB"
DATABASE_URL = "Вставить строку коннекта в бд postqgresql"

```

### Теперь можно запускать сервис
```commandline
uvicorn main:app --reload --port 8080
```

### Для запуска самого процесса парсинга 
нужно открыть в браузере страницу 
http://127.0.0.1:8080/docs

Откроется страница swager

далее запустить ендпойн start-collection/

