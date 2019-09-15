# coding: utf-8
import logging
import yaml

from tapioca_yandex_metrika import YandexMetrikaLogsapi

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]

api = YandexMetrikaLogsapi(
    access_token=ACCESS_TOKEN,
    default_url_params={'counterId': 178620}
)


def test_info():
    api.create().info()


def test_get_stats():
    r = api.allinfo({'counterId': 178620}).get()
    print(r)
    print(r().data)

