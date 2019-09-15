# coding: utf-8
import json
import logging
import time

from tapioca import TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin
from tapioca.exceptions import ResponseProcessException, ClientError

from tapioca_yandex_metrika import exceptions
from .resource_mapping import (
    STATS_RESOURCE_MAPPING,
    LOGSAPI_RESOURCE_MAPPING,
    MANAGEMENT_RESOURCE_MAPPING
)


class YandexMetrikaManagementClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    resource_mapping = MANAGEMENT_RESOURCE_MAPPING

    def get_api_root(self, api_params):
        return "https://api-metrika.yandex.net/"

    def get_request_kwargs(self, api_params, *args, **kwargs):
        """Обогащение запроса, параметрами"""
        params = super().get_request_kwargs(api_params, *args, **kwargs)
        params["headers"]["Authorization"] = "OAuth {}".format(api_params["access_token"])
        return params

    def get_error_message(self, data, response=None):
        try:
            if not data and response.content.strip():
                data = json.loads(response.content.decode("utf-8"))

            if data:
                return data.get("message")
        except json.JSONDecodeError:
            return response.text

    def process_response(self, response, **request_kwargs):
        # При ошибке 500 и в других в ответах может быть json с ошибками.
        data = self.response_to_native(response)

        if isinstance(data, dict) and data.get("errors"):
            raise ResponseProcessException(ClientError, data)
        else:
            data = super().process_response(response)

        return data

    def response_to_native(self, response):
        if response.content.strip():
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text

    def wrapper_call_exception(
        self, response, tapioca_exception, api_params, *args, **kwargs
    ):
        try:
            jdata = response.json()
        except json.JSONDecodeError:
            raise exceptions.YandexMetrikaApiError(response)
        else:
            error_code = int(jdata.get("code", 0))

            if error_code == 429:
                raise exceptions.YandexMetrikaLimitError(response)
            elif error_code == 403:
                raise exceptions.YandexMetrikaTokenError(response)
            else:
                raise exceptions.YandexMetrikaClientError(response)

    def data(self, data, request_kwargs, response, api_params):
        return data[0] if isinstance(data, list) and data else data


class YandexMetrikaLogsapiClientAdapter(YandexMetrikaManagementClientAdapter):
    resource_mapping = LOGSAPI_RESOURCE_MAPPING


class YandexMetrikaStatsClientAdapter(YandexMetrikaManagementClientAdapter):
    resource_mapping = STATS_RESOURCE_MAPPING

    def retry_request(self, response, tapioca_exception, api_params, count_request_error, *args, **kwargs):
        """
        Условия повторения запроса.

        response = tapioca_exception.client().response
        status_code = tapioca_exception.client().status_code
        response_data = tapioca_exception.client().data
        """
        status_code = tapioca_exception.client().status_code
        response_data = tapioca_exception.client().data
        error_code = int((response_data or {}).get("code", 0))

        if error_code == 429:
            logging.error("Превышен лимит запросов")
        elif error_code == 503:
            if count_request_error < api_params.get("retries_if_server_error", 3):
                logging.warning('Серверная ошибка. Повторный запрос через 3 секунды')
                time.sleep(3)
                return True

        return False

    def extra_request(
        self, api_params, current_request_kwargs, request_kwargs_list, response, current_result
    ):
        total_rows = int(current_result['total_rows'])
        sampled = current_result['sampled']

        logging.info('Наличие семплирования: ' + str(sampled))

        limit = current_result["query"]["limit"]
        offset = current_result["query"]["offset"] + limit

        if offset <= total_rows:
            if api_params.get("receive_all_data", False):
                logging.warning('Получены не все данные. Будет сделан дополнительный запрос')
                new_request_kwargs = current_request_kwargs.copy()
                new_request_kwargs["params"]["offset"] = offset
                request_kwargs_list.append(new_request_kwargs)
            else:
                logging.warning("Получены не все данные")
        return request_kwargs_list

    def transform(self, results, request_kwargs, *args, **kwargs):
        """Преобразование данных"""
        new_data = []
        columns = results[0]["query"]["dimensions"] + results[0]["query"]["metrics"]
        for result in results:
            data = result.pop("data")
            for row in data:
                dimensions = [i["name"] for i in row["dimensions"]]
                metrics = row["metrics"]
                new_data.append(dimensions + metrics)
        return [columns] + new_data

    def data(self, data, request_kwargs, response, api_params):
        return data


YandexMetrikaStats = generate_wrapper_from_adapter(YandexMetrikaStatsClientAdapter)
YandexMetrikaLogsapi = generate_wrapper_from_adapter(YandexMetrikaLogsapiClientAdapter)
YandexMetrikaManagement = generate_wrapper_from_adapter(YandexMetrikaManagementClientAdapter)
