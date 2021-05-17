# Documentation for downloading reports from Yandex Metrika LOGS API

[Official documentation Yandex Metrika LOGS API](https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html)

```python
from tapi_yandex_metrika import YandexMetrikaLogsapi

ACCESS_TOKEN = ""
COUNTER_ID = ""

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

    # Transform to dicts
    print(part().to_dicts()[:3])
else:
    print("Report not ready yet")
```

## Automatically download the report when it is prepared

add param **wait_report**

```python
from tapi_yandex_metrika import YandexMetrikaLogsapi

ACCESS_TOKEN = ""
COUNTER_ID = ""

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

print("Raw data")
data = report.data

print("Column names")
print(report.columns)

# Transform to values
print(report().to_values())

# Transform to lines
print(report().to_lines())

# Transform to dict
print(report().to_dicts())
```

## Export of all report parts.
```python
report = client.download(requestId=request_id).get()

print(report.columns)

# Iteration parts.
for part in report().parts():
    print(part.data)  # raw data
    print(part().to_values())
    print(part().to_lines())
    print(part().to_columns())  # columns data orient
    print(part().to_dicts())

for part in report().parts():
    # Iteration lines.
    for row_as_text in part().lines():
        print(row_as_text)

    # Iteration values.
    for row_as_values in part().values():
        print(row_as_values)

    # Iteration dicts.
    for row_as_dict in part().dicts():
        print(row_as_dict)


```

## Iterate all rows of all parts of the report

Will iterate over all lines of all parts

```python
report = client.download(requestId=request_id).get()

print(report.columns)

for row_as_line in report().iter_lines():
    print(row_as_line)

for row_as_values in report().iter_values():
    print(row_as_values)

for row_as_dict in report().iter_dicts():
    print(row_as_dict)
```

## Limit iteration

    .parts(max_parts: int = None)
    .lines(max_rows: int = None)
    .values(max_rows: int = None)
    .iter_lines(max_parts: int = None, max_rows: int = None)
    .iter_values(max_parts: int = None, max_rows: int = None)

## Response

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

## Warning
Pay attention to which HTTP method you send the request.
Some resources work only with POST or only with GET requests.
For example create resource with POST method only

    client.create().post(params=params)

And evaluate method only with GET method

    client.evaluate().get(params=params)


## AUTHORS
Pavel Maksimov -
[Telegram](https://t.me/pavel_maksimow),
[Facebook](https://www.facebook.com/pavel.maksimow)

Good luck friend! Put an asterisk;)

Удачи тебе, друг! Поставь звездочку ;)

Copyright (c) Pavel Maksimov.


## CHANGELOG
### Release 2021.5.15
- add iteration method "dicts"
- add iteration method "iter_dicts"
- add method "to_dicts"
- rename parameter max_items to max_rows in iter_lines, iter_values, lines, values


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
