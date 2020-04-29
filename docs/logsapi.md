## Документация по Logs API
```python
from tapi_yandex_metrika import YandexMetrikaLogsapi


ACCESS_TOKEN = {ваш токен доступа}
COUNTER_ID = {идентификатор счетчика}

api = YandexMetrikaLogsapi(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID}
)

params={
    "fields": "ym:s:date,ym:s:clientID",
    "source": "visits",
    "date1": "2019-01-01",
    "date2": "2019-01-01"
}

# Проверить возможность создания отчета. Через HTTP метод GET.
result = api.evaluate().get(params=params)
print(result)


# Заказать отчет. Через HTTP метод POST.
result = api.create().post(params=params)
request_id = result().data["log_request"]["request_id"]
print(result)


# Отменить создание отчета. Через HTTP метод POST.
result = api.cancel(requestId=request_id).post()
print(result)


# Удалить отчет. Через HTTP метод POST.
result = api.clean(requestId=request_id).post()
print(result)


# Получить информацию обо всех отчетах хранящихся на сервере. Через HTTP метод GET.
result = api.allinfo().get()
print(result)


# Получить информацию о конкретном отчете. Через HTTP метод GET.
result = api.info(requestId=request_id).get()
print(result)


# Скачать отчет. Через HTTP метод POST.
result = api.create().post(params=params)
request_id = result().data["log_request"]["request_id"]

# Отчет можно скачать, когда он будет сформирован на сервере. Через HTTP метод GET.
result = api.info(requestId=request_id).get()
if result["log_request"]["status"] == "processed":
    # Отчет может состоять из нескольких частей.
    parts = result["log_request"]["parts"]  # Кол-во частей в отчете.
    print("Кол-во частей", parts)
    # В параметр partNumber указывается номер части отчета, который хотите скачать.
    # Скачаем первую часть.
    result = api.download(requestId=request_id, partNumber=0).get()
    data = result().data
    print(data[:1000])
else:
    print("Отчет еще не готов")
```

В библиотеке есть функция, которая
подождет, когда отчет будет сформирован и скачает все его части.
```python
from tapi_yandex_metrika import YandexMetrikaLogsapi

ACCESS_TOKEN = {ваш токен доступа}
COUNTER_ID = {идентификатор счетчика}

api = YandexMetrikaLogsapi(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID},
    # Если True, скачает первую часть отчета, когда он будет сформирован.
    # По умолчанию False.
    wait_report=True,
    # Если True, будет скачивать все части отчета.
    # По умолчанию False.
    receive_all_data=True
)
params={
    "fields": "ym:s:date,ym:s:clientID,ym:s:dateTime,ym:s:startURL,ym:s:endURL",
    "source": "visits",
    "date1": "2019-01-01",
    "date2": "2019-01-01"
}
result = api.create().post(params=params)
request_id = result().data["log_request"]["request_id"]
# Когда включен параметр receive_all_data=True, параметр partNumber можно не указывать.
result = api.download(requestId=request_id).get()
data = result().data
print(data[:1000])
```

Есть метод преобразования данных для ресурса **download**.
```python
result = api.download(requestId=request_id).get()
data_as_json = result().transform()
print(data_as_json[:2])
[
    ['ym:s:date', 'ym:s:startOfMonth', 'ym:s:visits', 'ym:s:bounces'],
    ['2019-09-26', '2019-09-01', 80384.0, 9389.0]
 ]
```

Можно получить информацию о последнем сделанном запросе

```python
result = api.allinfo().get()
print(result().status_code)
print(result().response)
print(result().response.headers)
```

Обращайте внимание каким HTTP методом вы отправляете запрос.
Некоторые ресурсы работают только с POST или только с GET запросами.
Например ресурс **create** только с методом POST

    api.create().post(params=params)

А метод **evaluate** только с методом GET

    api.evaluate().get(params=params)


## Фичи

Можно вывести на печать описание ресурса через метод info
```python
# Указываете интересующий ресурс, а после него .info()
api.create().info()
```

Открыть документацию ресурса в браузере
```python
api.create().open_docs()
```

## Автор
Павел Максимов

Связаться со мной можно в
[Телеграм](https://t.me/pavel_maksimow)
и в
[Facebook](https://www.facebook.com/pavel.maksimow)

Удачи тебе, друг! Поставь звездочку ;)
