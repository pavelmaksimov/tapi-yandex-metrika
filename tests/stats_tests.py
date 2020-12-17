import datetime as dt
import logging
import mock
import requests
import yaml
from tapi2.adapters import TapiAdapter

from tapi_yandex_metrika import YandexMetrikaStats

logging.basicConfig(level=logging.DEBUG)

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]
COUNTER_ID = data_loaded["counter_id"]

api = YandexMetrikaStats(access_token=ACCESS_TOKEN)


def test_info():
    api.stats().help()


def test_stats():
    params = dict(
        ids=COUNTER_ID,
        metrics="ym:s:visits",
        filters="ym:s:startURL=.('https://rfgf.ru/map','https://rfgf.ru/map')",
        limit=1,
    )
    r = api.stats().get(params=params)
    print(r.data)
    print(r.response)


def test_transform():
    params = dict(
        ids=100500,
        metrics="ym:s:visits",
        dimensions="ym:s:date",
        sort="ym:s:date",
        group='Day',
        date1=dt.date(2020, 10, 1),
        date2='2020-10-05',
        limit=1,
    )

    requests.sessions.Session.request = mock.Mock(return_value=None)
    response_data = {
        'query': {'ids': [100500], 'dimensions': ['ym:s:date'], 'metrics': ['ym:s:visits'], 'sort': ['ym:s:date'],
                  'date1': '2020-10-01', 'date2': '2020-10-05', 'limit': 1, 'offset': 1, 'group': 'Day',
                  'auto_group_size': '1', 'attr_name': '', 'quantile': '50', 'offline_window': '21',
                  'attribution': 'LastSign', 'currency': 'RUB', 'adfox_event_id': '0'},
        'data': [{'dimensions': [{'name': '2020-10-01'}], 'metrics': [14234.0]},
                 {'dimensions': [{'name': '2020-10-02'}], 'metrics': [12508.0]},
                 {'dimensions': [{'name': '2020-10-03'}], 'metrics': [12365.0]},
                 {'dimensions': [{'name': '2020-10-04'}], 'metrics': [14588.0]},
                 {'dimensions': [{'name': '2020-10-05'}], 'metrics': [14579.0]}], 'total_rows': 5,
        'total_rows_rounded': False, 'sampled': False, 'contains_sensitive_data': False, 'sample_share': 1.0,
        'sample_size': 68280, 'sample_space': 68280, 'data_lag': 4242, 'totals': [68274.0], 'min': [12365.0],
        'max': [14588.0]
    }
    TapiAdapter.process_response = mock.Mock(return_value=response_data)

    report = api.stats().get(params=params)

    assert report.data == response_data
    assert report().to_values() == [['2020-10-01', 14234.0],
                                    ['2020-10-02', 12508.0],
                                    ['2020-10-03', 12365.0],
                                    ['2020-10-04', 14588.0],
                                    ['2020-10-05', 14579.0]]
    assert report().to_columns() == [['2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05'],
                                     [14234.0, 12508.0, 12365.0, 14588.0, 14579.0]]


def test_iteration():
    requests.sessions.Session.request = mock.Mock(return_value=None)
    response_data = {
        'query': {
            'ids': [100500], 'dimensions': ['ym:s:date'], 'metrics': ['ym:s:visits'], 'sort': ['ym:s:date'],
            'date1': '2020-10-01', 'date2': '2020-10-05', 'limit': 1, 'offset': 1, 'group': 'Day',
            'auto_group_size': '1', 'attr_name': '', 'quantile': '50', 'offline_window': '21',
            'attribution': 'LastSign', 'currency': 'RUB', 'adfox_event_id': '0'
        },
        'data': [{'dimensions': [{'name': '2020-10-01'}], 'metrics': [14234.0]},
                 {'dimensions': [{'name': '2020-10-02'}], 'metrics': [12508.0]}, ], 'total_rows': 5,
        'total_rows_rounded': False, 'sampled': False, 'contains_sensitive_data': False, 'sample_share': 1.0,
        'sample_size': 68280, 'sample_space': 68280, 'data_lag': 4242, 'totals': [68274.0], 'min': [12365.0],
        'max': [14588.0]
    }
    TapiAdapter.process_response = mock.Mock(return_value=response_data)

    limit = 1
    params = dict(
        ids=100500,
        metrics="ym:s:visits",
        dimensions="ym:s:date",
        sort="ym:s:date",
        group='Day',
        date1=dt.date(2020, 10, 1),
        date2='2020-10-05',
        limit=limit,
    )
    report = api.stats().get(params=params)

    for page in report().pages():
        assert page.data == response_data
        for row in page().rows():
            assert isinstance(row, list)
            assert len(row) == 2

        response_data["query"]["offset"] += limit
        TapiAdapter.process_response = mock.Mock(return_value=response_data)

    i = 0
    for row in report().iter_rows():
        i += 1
        assert isinstance(row, list)
        assert len(row) == 2
    assert i == 2
