import logging
import yaml

from tapi_yandex_metrika import YandexMetrikaManagement

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]
COUNTER_ID = data_loaded["counter_id"]

api = YandexMetrikaManagement(
    access_token=ACCESS_TOKEN, default_url_params={"counterId": COUNTER_ID}
)


def test_info():
    print(dir(api))


def test_get_counters():
    r = api.counters().get(params={"sort": "Visits"})
    print(r.data)


def test_get_clients():
    r = api.clients().get(params={"counters": [COUNTER_ID]})
    print(r)


def test_get_goals():
    r = api.goals().get()
    global goal_id
    goal_id = r.data["goals"][0]["id"]
    print(r)


def test_get_goal():
    r = api.goal(goalId=goal_id).get()
    print(r)
