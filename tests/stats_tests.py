import datetime as dt
import logging

import responses
import yaml

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


@responses.activate
def test_transform():
    response_data = {
        "query": {
            "ids": [100500],
            "dimensions": ["ym:s:date"],
            "metrics": ["ym:s:visits"],
            "sort": ["ym:s:date"],
            "date1": "2020-10-01",
            "date2": "2020-10-05",
            "limit": 1,
            "offset": 1,
            "group": "Day",
            "auto_group_size": "1",
            "attr_name": "",
            "quantile": "50",
            "offline_window": "21",
            "attribution": "LastSign",
            "currency": "RUB",
            "adfox_event_id": "0",
        },
        "data": [
            {"dimensions": [{"name": "2020-10-01"}], "metrics": [14234.0]},
            {"dimensions": [{"name": "2020-10-02"}], "metrics": [12508.0]},
            {"dimensions": [{"name": "2020-10-03"}], "metrics": [12365.0]},
            {"dimensions": [{"name": "2020-10-04"}], "metrics": [14588.0]},
            {"dimensions": [{"name": "2020-10-05"}], "metrics": [14579.0]},
        ],
        "total_rows": 5,
        "total_rows_rounded": False,
        "sampled": False,
        "contains_sensitive_data": False,
        "sample_share": 1.0,
        "sample_size": 68280,
        "sample_space": 68280,
        "data_lag": 4242,
        "totals": [68274.0],
        "min": [12365.0],
        "max": [14588.0],
    }
    responses.add(
        responses.GET,
        "https://api-metrika.yandex.net/stat/v1/data?ids=100500&metrics=ym%3As%3Avisits&dimensions=ym%3As%3Adate&sort=ym%3As%3Adate&group=Day&date1=2020-10-01&date2=2020-10-05&limit=1",
        json=response_data,
        status=200,
    )
    params = dict(
        ids=100500,
        metrics="ym:s:visits",
        dimensions="ym:s:date",
        sort="ym:s:date",
        group="Day",
        date1=dt.date(2020, 10, 1),
        date2="2020-10-05",
        limit=1,
    )
    report = api.stats().get(params=params)

    assert report.data == response_data
    assert report().to_values() == [
        ["2020-10-01", 14234.0],
        ["2020-10-02", 12508.0],
        ["2020-10-03", 12365.0],
        ["2020-10-04", 14588.0],
        ["2020-10-05", 14579.0],
    ]
    assert report().to_columns() == [
        ["2020-10-01", "2020-10-02", "2020-10-03", "2020-10-04", "2020-10-05"],
        [14234.0, 12508.0, 12365.0, 14588.0, 14579.0],
    ]
    assert report().to_dicts() == [
        {"ym:s:date": "2020-10-01", "ym:s:visits": 14234.0},
        {"ym:s:date": "2020-10-02", "ym:s:visits": 12508.0},
        {"ym:s:date": "2020-10-03", "ym:s:visits": 12365.0},
        {"ym:s:date": "2020-10-04", "ym:s:visits": 14588.0},
        {"ym:s:date": "2020-10-05", "ym:s:visits": 14579.0},
    ]


@responses.activate
def test_iteration():
    resource_row = {"dimensions": [{"name": "2020-10-01"}], "metrics": [14234.0]}
    expected_row_list = ["2020-10-01", 14234.0]
    expected_row_dict = {"ym:s:date": "2020-10-01", "ym:s:visits": 14234.0}

    response_data = {
        "query": {
            "ids": [100500],
            "dimensions": ["ym:s:date"],
            "metrics": ["ym:s:visits"],
            "sort": ["ym:s:date"],
            "date1": "2020-10-01",
            "date2": "2020-10-05",
            "limit": 1,
            "offset": 1,
            "group": "Day",
            "auto_group_size": "1",
            "attr_name": "",
            "quantile": "50",
            "offline_window": "21",
            "attribution": "LastSign",
            "currency": "RUB",
            "adfox_event_id": "0",
        },
        "data": [resource_row, resource_row],
        "total_rows": 5,
        "total_rows_rounded": False,
        "sampled": False,
        "contains_sensitive_data": False,
        "sample_share": 1.0,
        "sample_size": 68280,
        "sample_space": 68280,
        "data_lag": 4242,
        "totals": [68274.0],
        "min": [12365.0],
        "max": [14588.0],
    }
    responses.add(
        responses.GET,
        "https://api-metrika.yandex.net/stat/v1/data?ids=100500&metrics=ym%3As%3Avisits&dimensions=ym%3As%3Adate&sort=ym%3As%3Adate&group=Day&date1=2020-10-01&date2=2020-10-05&limit=1",
        json=response_data,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api-metrika.yandex.net/stat/v1/data?ids=100500&metrics=ym%3As%3Avisits&dimensions=ym%3As%3Adate&sort=ym%3As%3Adate&group=Day&date1=2020-10-01&date2=2020-10-05&limit=1&offset=2",
        json=response_data,
        status=200,
    )
    limit = 1
    params = dict(
        ids=100500,
        metrics="ym:s:visits",
        dimensions="ym:s:date",
        sort="ym:s:date",
        group="Day",
        date1=dt.date(2020, 10, 1),
        date2="2020-10-05",
        limit=limit,
    )
    report = api.stats().get(params=params)

    for page in report().pages(max_pages=1):
        assert page.data == response_data

        for row in page().values():
            assert len(row) == 2
            assert row == expected_row_list

        for row in page().dicts():
            assert len(row) == 2
            assert row == expected_row_dict

        response_data["query"]["offset"] += limit

    i = 0
    for row in report().iter_values(max_pages=1):
        assert len(row) == 2
        assert row == expected_row_list
        i += 1
    assert i == 2

    for row in report().iter_dicts(max_pages=1):
        assert isinstance(row, dict)
        assert len(row) == 2
        assert row == expected_row_dict
