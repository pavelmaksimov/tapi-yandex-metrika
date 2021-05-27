import time

import responses
import yaml

from tapi_yandex_metrika import YandexMetrikaLogsapi

with open("../config.yml", "r") as stream:
    data_loaded = yaml.safe_load(stream)

ACCESS_TOKEN = data_loaded["token"]
COUNTER_ID = data_loaded["counter_id"]

api = YandexMetrikaLogsapi(
    access_token=ACCESS_TOKEN,
    default_url_params={"counterId": COUNTER_ID},
    wait_report=True,
)


def test_get_allinfo():
    r = api.allinfo().get()
    print(r)


def test_evaluate():
    r = api.evaluate().get(
        params={
            "fields": "ym:s:date",
            "source": "visits",
            "date1": "2020-12-01",
            "date2": "2020-12-01",
        }
    )
    print(r)


def test_create():
    r = api.create().post(
        params={
            "fields": "ym:s:date",
            # "fields": "ym:s:purchaseID,ym:s:purchaseDateTime,ym:s:purchaseAffiliation,ym:s:purchaseRevenue,ym:s:purchaseTax,ym:s:purchaseShipping,ym:s:purchaseCoupon,ym:s:purchaseCurrency,ym:s:purchaseProductQuantity,ym:s:productsPurchaseID,ym:s:productsID,ym:s:productsName,ym:s:productsBrand,ym:s:productsCategory,ym:s:productsCategory1,ym:s:productsCategory2,ym:s:productsCategory3,ym:s:productsCategory4,ym:s:productsCategory5,ym:s:productsVariant,ym:s:productsPosition,ym:s:productsPrice,ym:s:productsCurrency,ym:s:productsCoupon,ym:s:productsQuantity,ym:s:impressionsURL,ym:s:impressionsDateTime,ym:s:impressionsProductID,ym:s:impressionsProductName,ym:s:impressionsProductBrand,ym:s:impressionsProductCategory,ym:s:impressionsProductCategory1,ym:s:impressionsProductCategory2,ym:s:impressionsProductCategory3,ym:s:impressionsProductCategory4,ym:s:impressionsProductCategory5,ym:s:impressionsProductVariant,ym:s:impressionsProductPrice,ym:s:impressionsProductCurrency,ym:s:impressionsProductCoupon,ym:s:counterID,ym:s:clientID,ym:s:visitID,ym:s:watchIDs,ym:s:date,ym:s:dateTime,ym:s:dateTimeUTC,ym:s:clientTimeZone,ym:s:bounce,ym:s:pageViews,ym:s:visitDuration,ym:s:isNewUser,ym:s:startURL,ym:s:endURL,ym:s:UTMCampaign,ym:s:UTMContent,ym:s:UTMMedium,ym:s:UTMSource,ym:s:UTMTerm,ym:s:lastTrafficSource,ym:s:lastAdvEngine,ym:s:lastReferalSource,ym:s:lastSearchEngineRoot,ym:s:lastSearchEngine,ym:s:lastSocialNetwork,ym:s:lastSocialNetworkProfile,ym:s:referer,ym:s:hasGCLID,ym:s:lastDirectClickOrder,ym:s:lastDirectBannerGroup,ym:s:lastDirectClickBanner,ym:s:lastDirectPhraseOrCond,ym:s:lastDirectPlatformType,ym:s:lastDirectPlatform,ym:s:lastDirectConditionType,ym:s:lastCurrencyID,ym:s:regionCountry,ym:s:regionCity,ym:s:deviceCategory,ym:s:mobilePhone,ym:s:mobilePhoneModel,ym:s:goalsID,ym:s:goalsSerialNumber,ym:s:goalsDateTime,ym:s:goalsPrice,ym:s:goalsOrder",
            "source": "visits",
            "date1": "2020-12-01",
            "date2": "2020-12-01",
        }
    )
    global request_id
    request_id = r["log_request"]["request_id"]
    print(r)
    return request_id


def test_download():
    report = api.download(requestId=request_id).get()
    for part in report().parts(max_parts=2):
        for line in part().lines(max_rows=2):
            print("line", line)

        print("part", part().to_values()[:1])
        print("part", part().to_lines()[:1])

    print("report", report().to_values()[:1])
    print("report", report().to_lines()[:1])


def test_iter():
    report = api.download(requestId=request_id).get()
    for line in report().iter_lines(max_rows=2):
        print("line", line)

    for values in report().iter_values(max_rows=2):
        print("values", values)


def test_get_info():
    r = api.info(requestId=request_id).get()
    print(r)


def test_clean():
    request_id = test_create()
    while True:
        r = api.info(requestId=request_id).get()
        if r.data["log_request"]["status"] == "processed":
            break
        time.sleep(5)

    r = api.clean(requestId=request_id).post()
    print(r)


def test_cancel():
    request_id = test_create()
    r = api.cancel(requestId=request_id).post()
    print(r)


@responses.activate
def test_transform():
    response_data = (
        "col1\tcol2\n"
        "val1\tval2\n"
        "val11\tval22\n"
        "val111\tval222\n"
        "val1111\tval2222\n"
    )
    responses.add(
        responses.GET,
        "https://api-metrika.yandex.net/management/v1/counter/8011147/logrequest/0/part/0/download",
        body=response_data,
        status=200,
    )
    report = api.download(requestId=0).get()

    assert report.columns == ["col1", "col2"]
    assert report().to_values() == [
        ["val1", "val2"],
        ["val11", "val22"],
        ["val111", "val222"],
        ["val1111", "val2222"],
    ]
    assert report().to_lines() == [
        "val1\tval2",
        "val11\tval22",
        "val111\tval222",
        "val1111\tval2222",
    ]
    assert report().to_columns() == [
        ["val1", "val11", "val111", "val1111"],
        ["val2", "val22", "val222", "val2222"],
    ]
    assert report().to_dicts() == [
        {"col1": "val1", "col2": "val2"},
        {"col1": "val11", "col2": "val22"},
        {"col1": "val111", "col2": "val222"},
        {"col1": "val1111", "col2": "val2222"},
    ]


@responses.activate
def test_iteration():
    response_data = (
        "col1\tcol2\n"
        "val1\tval2\n"
        "val11\tval22\n"
        "val111\tval222\n"
        "val1111\tval2222\n"
    )
    responses.add(
        responses.GET,
        "https://api-metrika.yandex.net/management/v1/counter/8011147/logrequest/0/part/0/download",
        body=response_data,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api-metrika.yandex.net/management/v1/counter/8011147/logrequest/0/part/1/download",
        body=response_data,
        status=200,
    )

    columns = response_data.split("\n")[0].split("\t")
    expected_lines = response_data.split("\n")[1:]
    expected_values = [i.split("\t") for i in response_data.split("\n")[1:]]
    expected_dicts = [
        dict(zip(columns, i.split("\t"))) for i in response_data.split("\n")[1:]
    ]

    report = api.download(requestId=0).get()

    for part in report().parts(max_parts=1):
        assert 4 == len(list(part().lines()))
        assert 4 == len(list(part().values()))

        for line, expected in zip(part().lines(), expected_lines):
            assert line == expected

        for values, expected in zip(part().values(), expected_values):
            assert values == expected

        for values, expected in zip(part().dicts(), expected_dicts):
            assert values == expected

    for line, expected in zip(report().iter_lines(max_rows=3), expected_lines):
        assert line == expected

    for values, expected in zip(report().iter_values(max_rows=3), expected_values[:4]):
        assert values == expected

    for values, expected in zip(report().iter_dicts(max_rows=3), expected_dicts[:4]):
        assert values == expected
