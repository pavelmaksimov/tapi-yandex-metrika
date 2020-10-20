# coding: utf-8
import logging
import time

import yaml

from tapi_yandex_metrika import YandexMetrikaLogsapi

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]
COUNTER_ID = data_loaded["counter_id"]

api = YandexMetrikaLogsapi(
    access_token=ACCESS_TOKEN,
    default_url_params={"counterId": COUNTER_ID},
    wait_report=True,
    receive_all_data=True,
)


def test_get_allinfo():
    r = api.allinfo().get()
    print(r)


def test_evaluate():
    r = api.evaluate().get(
        params={
            "fields": "ym:s:date",
            "source": "visits",
            "date1": "2019-01-01",
            "date2": "2019-01-01",
        }
    )
    print(r)


def test_create():
    r = api.create().post(
        params={
            "fields": "ym:s:bounce",
            "source": "visits",
            "date1": "2020-04-17",
            "date2": "2020-04-17",
        }
    )
    global request_id
    request_id = r().data["log_request"]["request_id"]
    print(r)


def test_get_info():
    r = api.info(requestId=request_id).get()
    print(r)


def test_cancel():
    r = api.cancel(requestId=request_id).post()
    print(r)


def test_clean():
    test_create()

    while True:
        r_ = api.info(requestId=request_id).get()
        if r_().data["log_request"]["status"] == "processed":
            break
        time.sleep(5)

    r = api.clean(requestId=request_id).post()
    print(r)


def test_download():
    test_create()
    r = api.download(requestId=request_id).get()
    data = r().transform()
    print("\n", len(data), "\n", data[:5])
