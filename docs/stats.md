## Документация по скачиванию отчетов из Я.Метрика

``` python
from tapi_yandex_metrika import YandexMetrikaStats

ACCESS_TOKEN = {ваш токен доступа}
COUNTER_ID = {номер счетчика Я.Метрики}

api = YandexMetrikaStats(access_token=ACCESS_TOKEN)

params = dict(
    ids=COUNTER_ID,
    metrics="ym:s:visits,ym:s:bounces",
    dimensions="ym:s:date,ym:s:startOfMonth",
    sort="ym:s:date",
    limit=5
)
result = api.stats().get(params=params)
print(result().data)

# По умолчанию возвращаются только 10000 строк отчета,
# если не указать другое кол-во в параметре limit.
# В отчете может быть больше строк, чем указано в limit
# Тогда необходимо сделать несколько запросов для получения всего отчета.
# Чтоб сделать это автоматически вы можете указать
# параметр receive_all_data=True при инициализации класса.

api = YandexMetrikaStats(
    access_token=ACCESS_TOKEN,
    # Если True, будет скачивать все части отчета. По умолчанию False.
    receive_all_data=True
)
params = dict(
    ids=COUNTER_ID,
    metrics="ym:s:visits,ym:s:bounces",
    dimensions="ym:s:date,ym:s:startOfMonth",
    sort="ym:s:date",
    limit=10
)
result = api.stats().get(params=params)
print(result().data)
```

В params можно передать [много других параметров](https://yandex.ru/dev/metrika/doc/api2/api_v1/data-docpage/).

#### Получить данные ответа.
```python
result = api.stats().get(params=params)
data = result().data
print(data)
[{json_data}, {json_data},] # В списке может находится несколько ответов
```

##### Преобразование ответа

Для ответов API отчетов есть функция преобразования **transform**.
Она соединяет все ответы в один список.
```python
result = api.stats().get(params=params)
data = result().transform()
print(data)
[['ym:s:date', 'ym:s:startOfMonth', 'ym:s:visits', 'ym:s:bounces'],
 ['2019-09-26', '2019-09-01', 80384.0, 9389.0]]
```

Можно получить информацию о последнем запросе.
```python
print(result().status_code)
print(result().response)
print(result().response.headers)
```

## Фичи

Вывести описание ресурса
```python
# Указываете интересующий ресурс, а после него .info()
api.stats().info()
```

Открыть документацию ресурса в браузере
```python
api.stats().open_docs()
```

Послать запрос в браузере
```python
api.stats().open_in_browser()
```

## Автор
Павел Максимов

Связаться со мной можно в
[Телеграм](https://t.me/pavel_maksimow)
и в
[Facebook](https://www.facebook.com/pavel.maksimow)

Удачи тебе, друг! Поставь звездочку ;)
