# coding: utf-8
import datetime as dt
import logging
from pprint import pprint
import yaml

from tapioca_yandex_metrika import YandexMetrikaStats

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]

api = YandexMetrikaStats(
    access_token=ACCESS_TOKEN,
    receive_all_data=True
)


def test_info():
    api.stats().info()


def test_get_stats():
    params = dict(
        ids="178620",
        metrics="ym:s:visits,ym:s:bounces",
        dimensions="ym:s:date,ym:s:startOfMonth",
        sort="ym:s:date",
        limit=5
    )
    r = api.stats().get(params=params)
    print()
    print(r)
    print()
    print(r().data)
    print()
    pprint(r().transform())

