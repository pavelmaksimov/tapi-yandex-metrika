## Документация по API управления счетчиком Я.Метрики

``` python
from tapi_yandex_metrika import YandexMetrikaManagement

ACCESS_TOKEN = {ваш токен доступа}
COUNTER_ID = {идентификатор счетчика}

api = YandexMetrikaManagement(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID}
)
```

Генерация класса YandexMetrikaManagement происходит динамически, поэтому узнать о добавленных ресурсах API, можно так.

    print(dir(api))

Пример

```python
# Получить счетчики. Через HTTP метод GET.
api.counters().get()

# Получить счетчики с сортировкой по визитам. Через HTTP метод GET.
api.counters().get(params={"sort": "Visits"})

# Создать цель. Через HTTP метод POST.
body = {
        "goal": {
            "name": "2 страницы",
            "type": "number",
            "is_retargeting": 0,
            "depth": 2
        }
    }
api.goals().post(data=body)

# Для некоторых ресурсов необходимо подставлять в url идентификатор объекта.
# Это делается путем добавления в сам метод идентификатора.
# Получить информацию о цели. Через HTTP метод GET.
api.goal(goalId=10000).get()

# Изменить цель. Через HTTP метод PUT.
body = {
    "goal" : {
        "id" :  10000,
        "name" :  <string> ,
        "type" :  <goal_type>,
        "is_retargeting" :  <boolean>,
        ...
    }
}
api.goal(goalId=10000).put(data=body)

# Удалить цель. Через HTTP метод DELETE.
api.goal(goalId=10000).delete()
```

Доступные параметры ресурсов и идентификаторы объектов, которые нужно обязательно указывать в методе, ищите в
[справке](https://yandex.ru/dev/metrika/doc/api2/management/intro-docpage/)
и/или в [карте ресурсов](https://github.com/pavelmaksimov/tapi-yandex-metrika/blob/master/tapi_yandex_metrika/resource_mapping.py).


#### Получить данные ответа.
```python
result = api.counters().get()
data = result().data
print(data)
```

Можно получить информацию о запросе.
```python
print(result)
print(result().status_code)
print(result().response)
print(result().response.headers)
```

## Фичи

Открыть документацию ресурса в браузере
```python
api.counters().open_docs()
```

Послать запрос в браузере
```python
api.counters().open_in_browser()
```

## Автор
Павел Максимов

Связаться со мной можно в
[Телеграм](https://t.me/pavel_maksimow)
и в
[Facebook](https://www.facebook.com/pavel.maksimow)

Удачи тебе, друг! Поставь звездочку ;)
