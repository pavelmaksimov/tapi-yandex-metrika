# coding: utf-8
import logging
from pprint import pprint

import yaml

from tapi_yandex_metrika import YandexMetrikaStats

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]
COUNTER_ID = data_loaded["counter_id"]

api = YandexMetrikaStats(access_token=ACCESS_TOKEN, receive_all_data=False)


def test_info():
    api.stats().info()


def test_get_stats():
    params = dict(
        ids=COUNTER_ID,
        metrics="ym:s:visits,ym:s:bounces",
        dimensions="ym:s:startOfHour",
        sort="ym:s:startOfHour",
        filters="ym:s:hour==10",
        date1="yesterday",
        date2="yesterday",
        group="hour",
        accuracy="full",
        attribution="lastsign",
        limit=10,
    )
    r = api.stats().get(params=params)
    print(r().data)
    print("после преобразования\n")
    pprint(r().transform())
