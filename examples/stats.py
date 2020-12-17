import datetime as dt
import logging
import yaml

from tapi_yandex_metrika import YandexMetrikaStats

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]
COUNTER_ID = data_loaded["counter_id"]

api = YandexMetrikaStats(access_token=ACCESS_TOKEN)


params = dict(
    ids=COUNTER_ID,
    date1="2020-10-01",
    date2=dt.date(2020,10,6),
    metrics="ym:s:visits",
    dimensions="ym:s:date",
    sort="ym:s:date",
    limit=5
    # Other params -> https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html
)
report = api.stats().get(params=params)

# Response data
print(report.data)

print(report.columns)
# ['ym:s:date', 'ym:s:visits']

print(report().to_values())
#[
#    ['2020-10-01', 14234.0],
#    ['2020-10-02', 12508.0],
#    ['2020-10-03', 12365.0],
#    ['2020-10-04', 14588.0],
#    ['2020-10-05', 14579.0]
#]


print(report().to_columns())
#[
#    ['2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05'],
#    [14234.0, 12508.0, 12365.0, 14588.0, 14579.0]
#]


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
