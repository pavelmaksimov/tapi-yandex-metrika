# Documentation for downloading reports from Yandex Metrika LOGS API

[Official documentation Yandex Metrika LOGS API](https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html)

```python
from tapi_yandex_metrika import YandexMetrikaLogsapi

ACCESS_TOKEN = <access_token>
COUNTER_ID = <counter_id>

client = YandexMetrikaLogsapi(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID}
)

params = {
    "fields": "ym:s:date,ym:s:clientID",
    "source": "visits",
    "date1": "2021-01-01",
    "date2": "2021-01-01"
}

# Check the possibility of creating a report. Via HTTP GET method.
result = client.evaluate().get(params=params)
print(result)


# Order a report. Via HTTP POST method.
result = client.create().post(params=params)
request_id = result["log_request"]["request_id"]
print(result)


# Cancel report creation. Via HTTP POST method.
result = client.cancel(requestId=request_id).post()
print(result)


# Delete report. Via HTTP POST method.
result = client.clean(requestId=request_id).post()
print(result)


# Get information about all reports stored on the server. Via HTTP GET method.
result = client.allinfo().get()
print(result)


# Get information about a specific report. Via HTTP GET method.
result = client.info(requestId=request_id).get()
print(result)


# Download the report. Via HTTP POST method.
result = client.create().post(params=params)
request_id = result["log_request"]["request_id"]

# The report can be downloaded when it is generated on the server. Via HTTP GET method.
info = client.info(requestId=request_id).get()
if info["log_request"]["status"] == "processed":

    # The report can consist of several parts.
    parts = info["log_request"]["parts"]
    print("Number of parts in the report", parts)

    # The partNumber parameter specifies the number of the part of the report that you want to download.
    # Default partNumber=0
    part = client.download(requestId=request_id, partNumber=0).get()

    print("Raw data")
    data = part.data[:1000]

    print("Column names")
    print(part.columns)

    # Transform to values
    print(part().to_values()[:3])

    # Transform to lines
    print(part().to_lines()[:3])
else:
    print("Report not ready yet")
```

#### Download the report when it will be created

add param **wait_report**

```python
from tapi_yandex_metrika import YandexMetrikaLogsapi

ACCESS_TOKEN = {ваш токен доступа}
COUNTER_ID = {идентификатор счетчика}

api = YandexMetrikaLogsapi(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': COUNTER_ID},
    # Download the report when it will be created
    wait_report=True,
)
params={
    "fields": "ym:s:date,ym:s:clientID,ym:s:dateTime,ym:s:startURL,ym:s:endURL",
    "source": "visits",
    "date1": "2019-01-01",
    "date2": "2019-01-01"
}
info = client.create().post(params=params)
request_id = info["log_request"]["request_id"]

report = client.download(requestId=request_id).get()

print("Column names")
print(report.columns)

print("Raw data")
data = report.data[:1000]

# Transform to values
print(report().to_values()[:3])

# Transform to lines
print(report().to_lines()[:3])
```

#### Export of all report pages.
```python
# Iteration parts.
report = client.download(requestId=request_id).get()
print(report.columns)
for part in report().parts():
    print(part.data[:1000])
    print(part().to_values()[:3])
    print(part().to_lines()[:3])
    print(part().to_columns()) # columns data orient

for part in report().parts():
    # Iteration lines.
    for line in part().lines():
        print('line', line)

    # Iteration values.
    for values in part().values():
        print('values', values)


# "Will iterate over all lines of all parts"

report = client.download(requestId=request_id).get()
print(report.columns)

for line in report().iter_lines():
    print('line', line)

for values in report().iter_values():
    print('values', values)
```

#### Limit iteration

    .parts(max_parts: int = None)
    .lines(max_items: int = None)
    .values(max_items: int = None)
    .iter_lines(max_parts: int = None, max_items: int = None)
    .iter_values(max_parts: int = None, max_items: int = None)

#### Resonse

```python
info = client.allinfo().get()
print(info.response)
print(info.response.headers)
print(info.response.status_code)

report = client.download(requestId=request_id).get()
for part in report().parts():
    print(part.response)
    print(part.response.headers)
    print(part.response.status_code)
```

#### Warning
Pay attention to which HTTP method you send the request.
Some resources work only with POST or only with GET requests.
For example create resource with POST method only

    client.create().post(params=params)

And evaluate method only with GET method

    client.evaluate().get(params=params)


## Authors
Pavel Maksimov -
[Telegram](https://t.me/pavel_maksimow),
[Facebook](https://www.facebook.com/pavel.maksimow)

Good luck friend! Put an asterisk;)

Удачи тебе, друг! Поставь звездочку ;)

Copyright (c) Pavel Maksimov.

## Change log
### Release 2021.2.21

**Backward Incompatible Change**

- Drop method "transform"
- Drop param "receive_all_data"

**New Feature**
- translated into english
- add iteration method "parts"
- add iteration method "lines"
- add iteration method "values"
- add iteration method "iter_lines"
- add iteration method "iter_values"
- add attribut "columns"
- add attribut "data"
- add attribut "response"
- add method "to_lines"
- add method "to_values"
- add method "to_columns"
