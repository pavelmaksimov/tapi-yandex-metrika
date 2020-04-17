# coding: utf-8
import json
import logging
import time
import re

from tapi import TapiAdapter, generate_wrapper_from_adapter, JSONAdapterMixin
from tapi.exceptions import ResponseProcessException, ClientError

from tapi_yandex_metrika import exceptions
from .resource_mapping import (
    STATS_RESOURCE_MAPPING,
    LOGSAPI_RESOURCE_MAPPING,
    MANAGEMENT_RESOURCE_MAPPING,
)

logging.basicConfig(level=logging.INFO)


class YandexMetrikaManagementClientAdapter(JSONAdapterMixin, TapiAdapter):
    resource_mapping = MANAGEMENT_RESOURCE_MAPPING

    def get_api_root(self, api_params):
        return "https://api-metrika.yandex.net/"

    def get_request_kwargs(self, api_params, *args, **kwargs):
        """Обогащение запроса, параметрами"""
        params = super().get_request_kwargs(api_params, *args, **kwargs)
        params["headers"]["Authorization"] = "OAuth {}".format(
            api_params["access_token"]
        )
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
        self, response, tapi_exception, api_params, *args, **kwargs
    ):
        try:
            jdata = response.json()
        except json.JSONDecodeError:
            raise exceptions.YandexMetrikaApiError(response)
        else:
            error_code = int(jdata.get("code", 0))
            message = jdata.get("message")

            if error_code == 429:
                raise exceptions.YandexMetrikaLimitError(response)
            elif error_code == 403:
                raise exceptions.YandexMetrikaTokenError(response)
            elif message == "Incorrect part number" and api_params.get(
                "receive_all_data", False
            ):
                # Срабатывает при попытке скачать несуществующую часть отчета.
                # А при получении всех частей отчета автоматически,
                # всегда идет попытка получить следующий часть.
                pass
            else:
                raise exceptions.YandexMetrikaClientError(response)

    def transform_results(self, results, request_kwargs, response, api_params):
        return results[0] if isinstance(results, list) and results else results


class YandexMetrikaLogsapiClientAdapter(YandexMetrikaManagementClientAdapter):
    resource_mapping = LOGSAPI_RESOURCE_MAPPING

    def transform_results(self, results, requests_kwargs, responses, api_params):
        if (
            api_params.get("receive_all_data", False)
            and responses[0].url.find("download") > -1
        ):
            # Собирает все части отчета в один текст.
            data, cols = "", ""
            for i in results:
                cols = i[:i.find("\n")]
                # Допонлительно удаляется пустая последняя строка.
                data += i[i.find("\n")+1:-1]
            return "{}\n{}\n".format(cols, data)
        else:
            return results[0] if isinstance(results, list) and results else results

    def transform(self, data, request_kwargs, response, api_params, *args, **kwargs):
        """Преобразование данных"""
        if response.url.find("download") > -1:
            return [i.split("\t") for i in data.split("\n")][:-1]
        else:
            raise NotImplementedError(
                "Преобразование в JSON доступно только для ответов ресурса download"
            )

    def retry_request(
        self,
        response,
        tapi_exception,
        api_params,
        count_request_error,
        *args,
        **kwargs
    ):
        """
        Условия повторения запроса.

        response = tapi_exception.client().response
        status_code = tapi_exception.client().status_code
        response_data = tapi_exception.client().data
        """
        status_code = tapi_exception.client().status_code
        response_data = tapi_exception.client().data or {}
        error_code = int((response_data).get("code", 0))
        message = response_data.get("message")

        if (
            message == "Only log of requests in status 'processed' can be downloaded"
            and api_params.get("wait_report", False)
            and response.url.find("download") > -1
        ):
            logging.info("Включен режим ожидания готовности отчета")
            logging.info(
                "Ожидание готовности отчета {} сек.".format(count_request_error * 20)
            )
            time.sleep(count_request_error * 20)
            return True

        return False

    def extra_request(
        self,
        api_params,
        current_request_kwargs,
        request_kwargs_list,
        response,
        current_result,
    ):
        if (
            api_params.get("receive_all_data", False)
            and response.url.find("download") > -1
        ):
            logging.info("Включен режим получения всех данных")
            logging.info("Будет сделан запрос на получение других частей отчета")
            url = current_request_kwargs["url"]
            part = int(re.findall(r"part/([0-9]*)/", url)[0])
            new_part = part + 1
            new_url = re.sub(r"part/[0-9]*/", "part/{}/".format(new_part), url)
            new_request_kwargs = {**current_request_kwargs, "url": new_url}
            request_kwargs_list.append(new_request_kwargs)

        return request_kwargs_list

    def fill_resource_template_url(self, template, params):
        if template.find("/part/") > -1 and not params.get("partNumber"):
            # Принудительно добавляет параметр partNumber, если его нет.
            params.update(partNumber=0)
        return template.format(**params)


class YandexMetrikaStatsClientAdapter(YandexMetrikaManagementClientAdapter):
    resource_mapping = STATS_RESOURCE_MAPPING

    def retry_request(
        self,
        response,
        tapi_exception,
        api_params,
        count_request_error,
        *args,
        **kwargs
    ):
        """
        Условия повторения запроса.

        response = tapi_exception.client().response
        status_code = tapi_exception.client().status_code
        response_data = tapi_exception.client().data
        """
        status_code = tapi_exception.client().status_code
        response_data = tapi_exception.client().data
        error_code = int((response_data or {}).get("code", 0))

        if error_code == 429:
            logging.error("Превышен лимит запросов")
        elif error_code == 503:
            if count_request_error < api_params.get("retries_if_server_error", 3):
                logging.warning("Серверная ошибка. Повторный запрос через 3 секунды")
                time.sleep(3)
                return True

        return False

    def extra_request(
        self,
        api_params,
        current_request_kwargs,
        request_kwargs_list,
        response,
        current_result,
    ):
        total_rows = int(current_result["total_rows"])
        sampled = current_result["sampled"]

        logging.info("Наличие семплирования: " + str(sampled))
        limit = current_request_kwargs["params"].get("limit", 10000)
        offset = current_result["query"]["offset"] + limit

        if offset <= total_rows:
            logging.warning(
                "Получено строк {}. Всего строк {}".format(offset-1, total_rows)
            )
            if api_params.get("receive_all_data", False):
                logging.warning("Будет сделан дополнительный запрос")
                new_request_kwargs = current_request_kwargs.copy()
                new_request_kwargs["params"]["offset"] = offset
                request_kwargs_list.append(new_request_kwargs)
        return request_kwargs_list

    def transform(self, data, request_kwargs, response, api_params, *args, **kwargs):
        """Преобразование данных"""
        new_data = []
        columns = data[0]["query"]["dimensions"] + data[0]["query"]["metrics"]
        for result in data:
            data = result.pop("data")
            for row in data:
                dimensions = [i["name"] for i in row["dimensions"]]
                metrics = row["metrics"]
                new_data.append(dimensions + metrics)
        return [columns] + new_data

    def transform_results(self, results, request_kwargs, response, api_params):
        return results


YandexMetrikaStats = generate_wrapper_from_adapter(YandexMetrikaStatsClientAdapter)
YandexMetrikaLogsapi = generate_wrapper_from_adapter(YandexMetrikaLogsapiClientAdapter)
YandexMetrikaManagement = generate_wrapper_from_adapter(YandexMetrikaManagementClientAdapter)
