# coding: utf-8
import logging
from pprint import pprint
import yaml

from tapi_yandex_metrika import YandexMetrikaStats

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]

api = YandexMetrikaStats(
    access_token=ACCESS_TOKEN,
    receive_all_data=False
)


def test_info():
    api.stats().info()


def test_get_stats():
    params = dict(
        ids="178620",
        metrics="ym:s:visits,ym:s:bounces",
        dimensions="ym:s:date,ym:s:startOfMonth",
        sort="ym:s:date",
        limit=3
    )
    r = api.stats().get(params=params)
    print()
    print(r)
    print()
    print(r().data)
    print()
    pprint(r().transform())


def test_get_stats2():
    params = dict(
        direct_client_logins="ya-ozon-travel1",
        ids="178620",
        metrics="ym:ad:clicks,ym:ad:RUBAdCost",
        dimensions="ym:ad:startOfHour,ym:ad:<attribution>DirectID,ym:ad:<attribution>DirectPhraseOrCond",
        sort="ym:ad:startOfHour",
        filters="ym:ad:hour==10",
        date1="today",
        date2="today",
        group="hour",
        accuracy="full",
        attribution="lastsign",
        limit=10
    )
    r = api.stats().get(params=params)
    import datetime as dt
    import re
    data = r().transform()
    pprint(data)

    def t(i):
        i[0] = dt.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S")
        i[1] = int(str(i[1] or 0).replace("N-", ""))
        i[2] = re.sub(r" -.*", "", i[2] or "")
        i[3] = int(i[3] or 0)
        i.insert(1, i[0].hour)

    data = list(map(t, data))

    pprint(data)
