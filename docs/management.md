# Yandex Metrika Counter Management API Documentation

[Official documentation API Yandex Metrika](https://yandex.ru/dev/metrika/doc/api2/management/intro.html)


```python
from tapi_yandex_metrika import YandexMetrikaManagement

ACCESS_TOKEN = ""
COUNTER_ID = ""

client = YandexMetrikaManagement(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID}
)
```

### Resources
```python
print(dir(client))
['accounts', 'chart_annotation', 'chart_annotations', 'clients', 'counter', 'counter_undelete',
 'counters', 'delegate', 'delegates', 'filter', 'filters', 'goal', 'goals', 'grant', 'grants', 'label',
 'labels', 'offline_conversions_calls_extended_threshold', 'offline_conversions_calls_uploading',
 'offline_conversions_calls_uploadings', 'offline_conversions_extended_threshold',
 'offline_conversions_upload', 'offline_conversions_upload_calls', 'offline_conversions_uploading',
 'offline_conversions_uploadings', 'operation', 'operations', 'public_grant', 'segment', 'segments',
 'set_counter_label', 'user_params_upload', 'user_params_uploading', 'user_params_uploading_confirm',
 'user_params_uploadings', 'yclid_conversions_upload', 'yclid_conversions_uploading',
 'yclid_conversions_uploadings']

# Help information about the method
client.counters().help()
# Documentation: https://yandex.ru/dev/metrika/doc/api2/management/direct_clients/getclients-docpage/
# Resource path: management/v1/clients
# Available HTTP methods:
# ['GET']
# Available query parameters:
# 'counters=<list>'

# Open resource documentation in a browser
client.counters().open_docs()
```

How to send different types of HTTP requests

:param params: querystring arguments in the URL\
:param data: send data in the body of the request
```python
# Send HTTP 'GET' request
client.counters().get(data: dict = None, params: dict = None)
# Send HTTP 'POST' request
client.counters().post(data: dict = None, params: dict = None)
# Send HTTP 'DELETE' request
client.counters().delete(data: dict = None, params: dict = None)
# Send HTTP 'PUT' request
client.counters().put(data: dict = None, params: dict = None)
# Send HTTP 'PATCH' request
client.counters().patch(data: dict = None, params: dict = None)
# Send HTTP 'OPTIONS' request
client.counters().options(data: dict = None, params: dict = None)
```

```python
from tapi_yandex_metrika import YandexMetrikaManagement

client = YandexMetrikaManagement(...)

# Get counters. Via HTTP GET method.
counters = client.counters().get()
print(counters.data)

# Get counters sorted by visit. Via HTTP GET method.
counters = client.counters().get(params={"sort": "Visits"})
print(counters.data)

# Create a goal. Via HTTP POST method.
body = {
        "goal": {
            "name": "2 страницы",
            "type": "number",
            "is_retargeting": 0,
            "depth": 2
        }
    }
client.goals().post(data=body)

# Create target on JavaScript event. Via HTTP POST method.
body2 = {
    "goal": {
        "name": "Название вашей цели в метрике",
        "type": "action",
        "is_retargeting": 0,
        "conditions": [
                {
                    "type": "exact",
                    "url": <your_value>
                }
            ]
        }
    }
client.goals().post(data=body2)

# For some resources, you need to substitute the object identifier in the url.
# This is done by adding an identifier to the method itself.
# Get information about the target. Via HTTP GET method.
client.goal(goalId=10000).get()

# Change target. Via HTTP PUT method.
body = {
    "goal" : {
        "id" : <int>,
        "name" :  <string> ,
        "type" :  <goal_type>,
        "is_retargeting" :  <boolean>,
        ...
    }
}
client.goal(goalId=10000).put(data=body)

# Delete target. Via HTTP DELETE method.
client.goal(goalId=10000).delete()
```

You can get information about the request.
```python
counters = client.counters().get()
print(counters.response)
print(counters.response.headers)
print(counters.status_code)
```


## Authors
Pavel Maksimov -
[Telegram](https://t.me/pavel_maksimow),
[Facebook](https://www.facebook.com/pavel.maksimow)

Good luck friend! Put an asterisk;)

Удачи тебе, друг! Поставь звездочку ;)

Copyright (c) Pavel Maksimov.

## CHANGELOG
### Release 2022.4.8
- No changes for this api


### Release 2021.5.28
- Add stub file (syntax highlighting)


### Release 2021.2.21

**New Feature**
- add attribut "data"
- add attribut "response"
