# coding: utf-8
import logging
import yaml

from tapioca_yandex_metrika import YandexMetrikaManagement

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]

api = YandexMetrikaManagement(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': 178620}
)


def test_info():
    api.counters().info()


def test_get_counters():
    r = api.counters().get()
    print(r)
    print(r().data)

