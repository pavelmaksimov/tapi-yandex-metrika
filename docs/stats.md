# Documentation for downloading reports from API Yandex Metrika (Как скачать данные из API Яндекс Метрика)

[Official documentation API Yandex Metrika](https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html)

```python
import datetime as dt
from tapi_yandex_metrika import YandexMetrikaStats

ACCESS_TOKEN = ""
COUNTER_ID = ""

client = YandexMetrikaStats(access_token=ACCESS_TOKEN)

params = dict(
    ids=COUNTER_ID,
    date1="2020-10-01",
    date2=dt.date(2020,10,5),
    metrics="ym:s:visits",
    dimensions="ym:s:date",
    sort="ym:s:date",
    limit=5
    # Other params -> https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html
)
report = client.stats().get(params=params)

# Raw data
report.data

report.columns
# ['ym:s:date', 'ym:s:visits']

report().to_values()
#[
#    ['2020-10-01', 14234.0],
#    ['2020-10-02', 12508.0],
#    ['2020-10-03', 12365.0],
#    ['2020-10-04', 14588.0],
#    ['2020-10-05', 14579.0]
#]

report().to_dicts()

# Column data orient
report().to_columns()
#[
#    ['2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05'],
#    [14234.0, 12508.0, 12365.0, 14588.0, 14579.0]
#]

```

## Export of all report pages.
``` python
print("iteration report pages")
for page in report().pages():
    # Raw data.
    print(page.data)

    print(page().to_dicts())
    print(page().to_columns())
    print(page().to_values())

print("iteration report pages")
for page in report().pages():
    print("iteration rows as values")
    for row_as_values_of_page in page().values():
        print(row_as_values_of_page)
    # ['2020-10-01', 14234.0]
    # ['2020-10-02', 12508.0]
    # ['2020-10-03', 12365.0]
    # ['2020-10-04', 14588.0]
    # ['2020-10-05', 14579.0]
    # ['2020-10-06', 12795.0]

    print("iteration rows as dict")
    for row_as_dict_of_page in page().dicts():
        print(row_as_dict_of_page)
```

## Iterate all rows of all parts of the report

Will iterate over all lines of all parts

```python
for values in report().iter_values():
    print(values)
# ['2020-10-01', 14234.0]
# ['2020-10-02', 12508.0]
# ['2020-10-03', 12365.0]
# ['2020-10-04', 14588.0]
# ['2020-10-05', 14579.0]
# ['2020-10-06', 12795.0]

for row_as_dict in report().iter_dicts():
    print(row_as_dict)
```

## Iteration limit.

    .pages(max_pages: int = None)
    .values(max_rows: int = None)
    .dicts(max_rows: int = None)
    .iter_values(max_pages: int = None, max_rows: int = None)
    .iter_dicts(max_pages: int = None, max_rows: int = None)

```python
print("iteration report rows with limit")
for page in report().pages(max_pages=2):
    for values in page().values(max_rows=2):
        print(values)
# ['2020-10-01', 14234.0]
# ['2020-10-02', 12508.0]
# ['2020-10-06', 12795.0]


print("Will iterate over all lines of all pages with limit")
for values in report().iter_values(max_pages=2, max_rows=1):
    print(values)
# ['2020-10-01', 14234.0]
```

## Response
```python
report = client.stats().get(params=params)
print(report.response)
print(report.response.status_code)
print(report.response.headers)

for page in report().pages():
    print(page.response)
    print(page.response.status_code)
    print(page.response.headers)
```


## AUTHORS
Pavel Maksimov -
[Telegram](https://t.me/pavel_maksimow),
[Facebook](https://www.facebook.com/pavel.maksimow)

Good luck friend! Put an asterisk;)

Удачи тебе, друг! Поставь звездочку ;)


## CHANGELOG
### Release 2021.5.27
- Add stub file (syntax highlighting)


### Release 2021.5.15
- add iteration method "iter_values"
- add iteration method "iter_dicts"
- add iteration method "values"
- add iteration method "dicts"
- add method "to_dicts"
- rename parameter max_items to max_rows in iter_rows



### Release 2021.2.21

**Backward Incompatible Change**

- Drop method "transform"
- Drop param "receive_all_data"

**New Feature**
- translated into english
- add iteration method "pages"
- add iteration method "rows"
- add iteration method "iter_rows"
- add attribut "columns"
- add attribut "data"
- add attribut "response"
- add method "to_values"
- add method "to_columns"

\
Copyright (c) Pavel Maksimov.
