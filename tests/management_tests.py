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
    api.goals().info()


def test_get_counters():
    r = api.counters().get(params={"sort": "Visits"})
    print(r)
    print(r().data)


def test_get_clients():
    r = api.clients().get()
    print(r)


def test_get_goals():
    r = api.goals().get()
    print(r)


def test_create_goal():
    body = {
        "goal": {
            "name": "2 страницы",
            "type": "number",
            "is_retargeting": 0,
            "depth": 2
        }
    }
    r = api.goals().post(data=body)
    print(r)


def test_get_goal():
    r = api.goal(goalId=13571870).get()
    print(r)
