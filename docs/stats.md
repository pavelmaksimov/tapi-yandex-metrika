[Official documentation API Yandex Metrika](https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html)

# Documentation for downloading reports from API Yandex Metrika (Как скачать данные из API Яндекс Метрика)

``` python
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

# Response data
print(report.data)

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

# Column data orient
report().to_columns()
#[
#    ['2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05'],
#    [14234.0, 12508.0, 12365.0, 14588.0, 14579.0]
#]

```

#### Export of all report pages.
``` python
print("Iteratin report pages")
for page in report().pages():
    page_values = page().to_values()
    print(page_values)
# [['2020-10-01', 14234.0], ['2020-10-02', 12508.0], ['2020-10-03', 12365.0], ['2020-10-04', 14588.0], ['2020-10-05', 14579.0]]
# [['2020-10-06', 12795.0]]


print("Iteratin report rows")
for page in report().pages():
    for row in page().rows():
        print(row)
# ['2020-10-01', 14234.0]
# ['2020-10-02', 12508.0]
# ['2020-10-03', 12365.0]
# ['2020-10-04', 14588.0]
# ['2020-10-05', 14579.0]
# ['2020-10-06', 12795.0]


print("Will iterate over all lines of all pages")
for row in report().iter_rows():
    print(row)
# ['2020-10-01', 14234.0]
# ['2020-10-02', 12508.0]
# ['2020-10-03', 12365.0]
# ['2020-10-04', 14588.0]
# ['2020-10-05', 14579.0]
# ['2020-10-06', 12795.0]
```

#### Iteration limit.

    .pages(max_pages: int = None)
    .rows(max_items: int = None)
    .iter_rows(max_pages: int = None, max_items: int = None)

``` python
print("Iteratin report rows with limit")
for page in report().pages(max_pages=2):
    for row in page().rows(max_items=2):
        print(row)
# ['2020-10-01', 14234.0]
# ['2020-10-02', 12508.0]
# ['2020-10-06', 12795.0]


print("Will iterate over all lines of all pages with limit")
for row in report().iter_rows(max_pages=2, max_items=1):
    print(row)
# ['2020-10-01', 14234.0]
```

#### Response
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
- add iteration method "pages"
- add iteration method "rows"
- add iteration method "iter_rows"
- add attribut "columns"
- add attribut "data"
- add attribut "response"
- add method "to_values"
- add method "to_columns"
