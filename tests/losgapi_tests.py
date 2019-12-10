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
    default_url_params={'counterId': 178620},
    wait_report=True,
    receive_all_data=False
)


def test_get_allinfo():
    r = api.allinfo().get()
    print(r)
    print(r().data)


def test_create():
    r = api.create().post(
        params={
            "fields": "ym:s:date,ym:s:clientID,ym:s:params,ym:s:startURL,ym:s:endURL,ym:s:dateTime,ym:s:goalsID,ym:s:goalsDateTime,ym:s:lastTrafficSource,ym:s:lastAdvEngine,ym:s:lastReferalSource,ym:s:lastSearchEngineRoot,ym:s:lastSearchEngine,ym:s:lastSocialNetwork,ym:s:lastSocialNetworkProfile,ym:s:referer,ym:s:browserLanguage,ym:s:browserCountry,ym:s:deviceCategory,ym:s:clientTimeZone,ym:s:operatingSystem",
            "source": "visits",
            "date1": "2019-09-03",
            "date2": "2019-09-03"
        }
    )
    print(r)


def test_get_info():
    r = api.info(requestId=4736887).get()
    print(r)


def test_cancel():
    r = api.cancel(requestId=4736887).post()
    print(r)


def test_clean():
    r = api.clean(requestId=4728343).post()
    print(r)


def test_evaluate():
    r = api.evaluate().get(
        params={
            "fields": "ym:s:date,ym:s:clientID",
            "source": "visits",
            "date1": "2019-01-01",
            "date2": "2019-01-01"
        }
    )
    print(r().data)


def test_download():
    r = api.download(requestId=5442820, partNumber=2).get()
    print(r().data[:500])
    jdata = r().transform()
    print(jdata[:2])
