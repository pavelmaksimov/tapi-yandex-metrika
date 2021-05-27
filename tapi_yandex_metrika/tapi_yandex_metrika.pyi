from typing import Union, List, Iterator

from requests import Response


class YandexMetrikaBaseMethods:
    @property
    def data(self) -> dict: ...
    @property
    def request_kwargs(self) -> dict: ...
    @property
    def response(self) -> Response: ...
    @property
    def status_code(self) -> int: ...
    def __getitem__(self, item) -> Union[dict, list]: ...
    def __iter__(self) -> Iterator: ...

class YandexMetrikaClientExecutor:
    def open_docs(self) -> YandexMetrikaClientExecutor:
        """Open API official docs of resource in browser."""
    def open_in_browser(self) -> YandexMetrikaClientExecutor:
        """Send a request in the browser."""
    def help(self) -> YandexMetrikaClientExecutor:
        """Print docs of resource."""
    def get(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaBaseMethods:
        """
        Send HTTP 'GET' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """
    def post(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaBaseMethods:
        """
        Send HTTP 'POST' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """
    def put(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaBaseMethods:
        """
        Send HTTP 'PUT' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """
    def putch(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaBaseMethods:
        """
        Send HTTP 'PUTCH' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """
    def delete(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaBaseMethods:
        """
        Send HTTP 'DELETE' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """
    def options(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaBaseMethods:
        """
        Send HTTP 'OPTIONS' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """

# Management

class YandexMetrikaManagement:
    def __init__(self, *, access_token: str, default_url_params: dict = None):
        """
        :param access_token: Access token.
        :param default_url_params: {"counterId": <int>}
        """
    def counters(self) -> YandexMetrikaClientExecutor:
        """
           https://yandex.ru/dev/metrika/doc/api2/management/counters/counters-docpage/
           Allowed HTTP methods for requesting a resource: GET, POST
           GET params a resource: [callback=<string>
        & [favorite=<boolean>]
        & [field=<string>]
        & [label_id=<integer>]
        & [offset=<int>]
        & [per_page=<int>]
        & [permission=<string>]
        & [reverse=<boolean>]
        & [search_string=<string>]
        & [sort=<counters_sort>]
        & [status=<counter_status>]
        & [type=<counter_type>]
        """
    def counter(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/counters/counter-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: [callback=<string>] & [field=<string>]
        """
    def counter_undelete(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/counters/undeletecounter-docpage/
        Allowed HTTP methods for requesting a resource: POST
        GET params a resource:
        """
    def goals(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/goals/goals-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: [callback=<string>] & [useDeleted=<boolean>]
        """
    def goal(
        self, *, goalId: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/goals/goal-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: [callback=<string>]
        """
    def accounts(self) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/accounts/accounts-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: [callback=<string>] & [user_login=<string>]
        """
    def clients(self) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/direct_clients/getclients-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: counters=<list>
        """
    def filters(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/filters/filters-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: [callback=<string>]
        """
    def filter(
        self, *, filterId: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/filters/filter-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: [callback=<string>]
        """
    def operations(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/operations/operations-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: [callback=<string>]
        """
    def operation(
        self, *, operationId: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/operations/operation-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: [callback=<string>]
        """
    def grants(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/grants/grants-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: [callback=<string>]
        """
    def grant(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/grants/grant-docpage/
        Allowed HTTP methods for requesting a resource: GET, PUT, DELETE
        GET params a resource: user_login=<string>
        """
    def public_grant(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/public-grants/addgrant-docpage/
        Allowed HTTP methods for requesting a resource: POST, DELETE
        GET params a resource:
        """
    def delegates(self) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/delegates/delegates-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: [callback=<string>]
        """
    def delegate(self) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/delegates/deletedelegate-docpage/
        Allowed HTTP methods for requesting a resource: DELETE
        GET params a resource: user_login=<string>
        """
    def labels(self) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/labels/getlabels-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: None
        """
    def label(self, *, labelId: Union[str, int]) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/labels/getlabel-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: None
        """
    def set_counter_label(
        self, *, labelId: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/links/setcounterlabel-docpage/
        Allowed HTTP methods for requesting a resource: POST, DELETE
        GET params a resource: None
        """
    def segments(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/segments/getsegmentsforcounter-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: None
        """
    def segment(
        self, *, segmentId: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/segments/getsegment-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: None
        """
    def user_params_uploadings(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/userparams/findall-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: None
        """
    def user_params_uploading(
        self, *, uploadingId: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/userparams/findbyid-docpage/
        Allowed HTTP methods for requesting a resource: GET, PUT
        GET params a resource: None
        """
    def user_params_upload(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/userparams/upload-docpage/
        Allowed HTTP methods for requesting a resource: POST
        GET params a resource: action=<user_params_uploading_action>
        """
    def user_params_uploading_confirm(
        self, *, uploadingId: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/userparams/confirm-docpage/
        Allowed HTTP methods for requesting a resource: POST
        GET params a resource: None
        """
    def chart_annotations(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/chart_annotation/findall-docpage/
        Allowed HTTP methods for requesting a resource: GET, POST
        GET params a resource: None
        """
    def chart_annotation(
        self, *, Id: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/chart_annotation/get-docpage/
        Allowed HTTP methods for requesting a resource: GET, DELETE, PUT
        GET params a resource: None
        """
    def yclid_conversions_uploadings(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/yclid-conversion/findall-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: [limit=<integer>] & [offset=<integer>
        """
    def yclid_conversions_uploading(
        self, *, Id: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/yclid-conversion/findbyid-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: None
        """
    def yclid_conversions_upload(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/yclid-conversion/upload-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: [comment=<string>]
        """
    def offline_conversions_uploadings(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findall-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: None
        """
    def offline_conversions_calls_uploadings(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findallcalluploadings-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: None
        """
    def offline_conversions_uploading(
        self, *, Id: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findbyid-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: None
        """
    def offline_conversions_calls_uploading(
        self, *, Id: Union[str, int], counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/findcalluploadingbyid-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: None
        """
    def offline_conversions_upload(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/upload-docpage/
        Allowed HTTP methods for requesting a resource: POST
        GET params a resource: client_id_type=<offline_conversion_uploading_client_id_type> & [comment=<string>]
        """
    def offline_conversions_upload_calls(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
           https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/uploadcalls-docpage/
           Allowed HTTP methods for requesting a resource: POST
           GET params a resource: client_id_type=<offline_conversion_uploading_client_id_type>
        & [comment=<string>]
        & [new_goal_name=<string>]
        """
    def offline_conversions_extended_threshold(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/enableextendedthreshold-docpage/
        Allowed HTTP methods for requesting a resource: POST, DELETE
        GET params a resource: None
        """
    def offline_conversions_calls_extended_threshold(
        self, *, counterId: Union[str, int] = None
    ) -> YandexMetrikaClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/management/offline_conversion/enablecallsextendedthreshold-docpage/
        Allowed HTTP methods for requesting a resource: POST, DELETE
        GET params a resource: None
        """

# Stats

class YandexMetrikaStatsPageIteratorResponse(YandexMetrikaBaseMethods):
    def to_values(self) -> List[tuple]: ...
    def to_columns(self) -> List[list]: ...
    def to_dicts(self) -> List[dict]: ...
    def values(self, *, max_rows: int = None) -> Iterator[list]: ...
    def dicts(self, *, max_rows: int = None) -> Iterator[dict]: ...

class YandexMetrikaStatsPageIteratorExecutor(YandexMetrikaBaseMethods):
    def __call__(self) -> YandexMetrikaStatsPageIteratorResponse: ...

class YandexMetrikaStatsResponse(YandexMetrikaBaseMethods):
    def pages(
        self, *, max_pages: int = None
    ) -> Iterator[YandexMetrikaStatsPageIteratorExecutor]: ...
    def iter_values(
        self, *, max_pages: int = None, max_rows: int = None
    ) -> Iterator[list]: ...
    def iter_dicts(
        self, *, max_pages: int = None, max_rows: int = None
    ) -> Iterator[dict]: ...
    def to_values(self) -> List[list]: ...
    def to_columns(self) -> List[list]: ...
    def to_dicts(self) -> List[dict]: ...

class YandexMetrikaStatsClientExecutorResponse(YandexMetrikaBaseMethods):
    def __call__(self) -> YandexMetrikaStatsResponse: ...
    @property
    def columns(self) -> List[str]: ...

class YandexMetrikaStatsClientExecutor:
    def open_docs(self) -> YandexMetrikaStatsClientExecutor:
        """Open API official docs of resource in browser."""
    def open_in_browser(self) -> YandexMetrikaStatsClientExecutor:
        """Send a request in the browser."""
    def help(self) -> YandexMetrikaStatsClientExecutor:
        """Print docs of resource."""
    def get(self, *, params: dict = None) -> YandexMetrikaStatsClientExecutorResponse:
        """
        https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html

        Send HTTP 'GET' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """

class YandexMetrikaStats:
    def __init__(self, *, access_token: str): ...
    def stats(self) -> YandexMetrikaStatsClientExecutor:
        """https://yandex.ru/dev/metrika/doc/api2/api_v1/data.html"""

# Logs

class YandexMetrikaLogsapiPageIteratorResponse(YandexMetrikaBaseMethods):
    @property
    def data(self) -> str: ...
    def to_values(self) -> List[tuple]: ...
    def to_columns(self) -> List[list]: ...
    def to_dicts(self) -> List[dict]: ...
    def to_lines(self) -> List[str]: ...
    def values(self, *, max_rows: int = None) -> Iterator[list]: ...
    def dicts(self, *, max_rows: int = None) -> Iterator[dict]: ...
    def lines(self, *, max_rows: int = None) -> Iterator[str]: ...

class YandexMetrikaLogsapiPageIteratorExecutor(YandexMetrikaBaseMethods):
    @property
    def data(self) -> str: ...
    def __call__(self) -> YandexMetrikaLogsapiPageIteratorResponse: ...

class YandexMetrikaLogsapiResponse(YandexMetrikaBaseMethods):
    @property
    def data(self) -> str: ...
    def parts(
        self, *, max_parts: int = None
    ) -> Iterator[YandexMetrikaLogsapiPageIteratorExecutor]: ...
    def iter_lines(
        self, *, max_parts: int = None, max_rows: int = None
    ) -> Iterator[str]: ...
    def iter_values(
        self, *, max_parts: int = None, max_rows: int = None
    ) -> Iterator[list]: ...
    def iter_dicts(
        self, *, max_parts: int = None, max_rows: int = None
    ) -> Iterator[dict]: ...
    def to_values(self) -> List[list]: ...
    def to_columns(self) -> List[list]: ...
    def to_dicts(self) -> List[dict]: ...
    def to_lines(self) -> List[str]: ...

class YandexMetrikaLogsapiClientExecutorResponse(YandexMetrikaBaseMethods):
    @property
    def data(self) -> Union[dict, str]: ...
    def __call__(self) -> YandexMetrikaLogsapiResponse: ...
    @property
    def columns(self) -> List[str]: ...

class YandexMetrikaLogsapiClientExecutor:
    def open_docs(self) -> YandexMetrikaLogsapiClientExecutor:
        """Open API official docs of resource in browser."""
    def open_in_browser(self) -> YandexMetrikaLogsapiClientExecutor:
        """Send a request in the browser."""
    def help(self) -> YandexMetrikaLogsapiClientExecutor:
        """Print docs of resource."""
    def get(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaLogsapiClientExecutorResponse:
        """
        Send HTTP 'GET' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """
    def post(
        self, *, params: dict = None, data: dict = None
    ) -> YandexMetrikaLogsapiClientExecutorResponse:
        """
        Send HTTP 'POST' request.

        :param params: querystring arguments in the URL
        :param data: send data in the body of the request
        """

class YandexMetrikaLogsapi:
    def __init__(
        self,
        *,
        access_token: str,
        default_url_params: dict = None,
        wait_report: bool = False,
    ):
        """
        :param access_token: Access token.
        :param default_url_params: {"counterId": <int>}
        :param wait_report: For the 'download' resource, it will wait for the report and download it.
        """
    def allinfo(self) -> YandexMetrikaLogsapiClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/logs/queries/getlogrequests-docpage/
        Allowed HTTP methods for requesting a resource: GET
        """
    def info(
        self, *, requestId: Union[int, str], counterId: Union[int, str] = None
    ) -> YandexMetrikaLogsapiClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/logs/queries/getlogrequest-docpage/
        Allowed HTTP methods for requesting a resource: GET
        """
    def download(
        self,
        *,
        requestId: Union[int, str],
        partNumber: int = 0,
        counterId: Union[int, str] = None,
    ) -> YandexMetrikaLogsapiClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/logs/queries/download-docpage/
        Allowed HTTP methods for requesting a resource: GET
        """
    def clean(
        self, *, requestId: Union[int, str], counterId: Union[int, str] = None
    ) -> YandexMetrikaLogsapiClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/logs/queries/clean-docpage/
        Allowed HTTP methods for requesting a resource: POST
        """
    def cancel(
        self, *, requestId: Union[int, str], counterId: Union[int, str] = None
    ) -> YandexMetrikaLogsapiClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/logs/queries/cancel-docpage/
        Allowed HTTP methods for requesting a resource: POST
        """
    def create(
        self, *, counterId: Union[int, str] = None
    ) -> YandexMetrikaLogsapiClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/logs/queries/createlogrequest-docpage/
        Allowed HTTP methods for requesting a resource: POST
        GET params a resource: ['date1', 'date2', 'fields', 'source']
        """
    def evaluate(
        self, *, counterId: Union[int, str] = None
    ) -> YandexMetrikaLogsapiClientExecutor:
        """
        https://yandex.ru/dev/metrika/doc/api2/logs/queries/evaluate-docpage/
        Allowed HTTP methods for requesting a resource: GET
        GET params a resource: ['date1', 'date2', 'fields', 'source']
        """
