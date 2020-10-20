# coding: utf-8
import json
import logging
import random
import re
import time

import simplejson
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
    resource_mapping = MANAGEMENT_RESOURCE_MAPPING  # карта ресурсов

    def get_api_root(self, api_params):
        return "https://api-metrika.yandex.net/"

    def get_request_kwargs(self, api_params, *args, **kwargs):
        """
        Обогащение запроса, параметрами.

        :param api_params: dict
        :return: dict
        """
        params = super().get_request_kwargs(api_params, *args, **kwargs)
        params["headers"]["Authorization"] = "OAuth {}".format(
            api_params["access_token"]
        )
        return params

    def get_error_message(self, data, response=None):
        """Извлечение комментария к ошибке запроса."""
        try:
            if not data and response.content.strip():
                data = json.loads(response.content.decode("utf-8"))

            if data:
                return data.get("message")
        except (json.JSONDecodeError, simplejson.JSONDecodeError):
            return response.text

    def process_response(self, response, **request_kwargs):
        """Обработка ответа запроса."""
        data = self.response_to_native(response)

        if isinstance(data, dict) and data.get("errors"):
            raise ResponseProcessException(ClientError, data)
        else:
            # Дополнительная обработка происходит в методе родительского класса.
            data = super().process_response(response)

        return data

    def response_to_native(self, response):
        """Преобразование ответа."""
        if response.content.strip():
            try:
                return response.json()
            except (json.JSONDecodeError, simplejson.JSONDecodeError):
                return response.text

    def wrapper_call_exception(
        self, response, tapi_exception, api_params, *args, **kwargs
    ):
        """
        Для вызова кастомных исключений.
        Когда например сервер отвечает 200,
        а ошибки передаются внутри json.
        """
        try:
            jdata = response.json()
        except (json.JSONDecodeError, simplejson.JSONDecodeError):
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

    def transform_results(self, results, requests_kwargs, responses, api_params):
        """
        Преобразователь данных после получения всех ответов.

        :param results: list : данные всех запросов
        :param requests_kwargs: list : параметры всех запросов
        :param responses: list : ответы всех запросов
        :param api_params: dict : входящие параметры класса
        :return: list
        """
        return results[0] if isinstance(results, list) and results else results


class YandexMetrikaLogsapiClientAdapter(YandexMetrikaManagementClientAdapter):
    resource_mapping = LOGSAPI_RESOURCE_MAPPING

    def transform_results(self, results, requests_kwargs, responses, api_params):
        """
        Преобразователь данных после получения всех ответов.

        :param results: list : данные всех запросов
        :param requests_kwargs: list : параметры всех запросов
        :param responses: list : ответы всех запросов
        :param api_params: dict : входящие параметры класса
        :return: list
        """
        if (
            api_params.get("receive_all_data", False)
            and responses[0].url.find("download") > -1
        ):
            # Собирает все части отчета в один.
            data, cols = "", ""
            for i in results:
                cols = i[: i.find("\n")]  # строка с именами столбцов
                # Данные без строки со столбцами.
                data += i[i.find("\n") + 1 :]
            return "{}\n{}".format(cols, data)
        else:
            return results[0] if isinstance(results, list) and results else results

    def transform(self, data, request_kwargs, response, api_params, *args, **kwargs):
        """Преобразование данных."""
        if response.url.find("download") > -1:
            json_data = [
                i.split("\t")
                for i in data.split("\n")
                if i != ""  # удаляется пустая последняя строка
            ]
            return json_data
        else:
            raise NotImplementedError(
                "Преобразование в JSON доступно только для ответов ресурса download"
            )

    def retry_request(
        self, response, tapi_exception, api_params, count_request_error, *args, **kwargs
    ):
        """
        Условия повторения запроса.
        Если вернет True, то запрос повторится.

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
            # Ошибка появляется при попытке скачать неготовый отчет.
            sleep_time = count_request_error * 20
            logging.info(
                "Включен режим ожидания готовности отчета. "
                "Проверка готовности отчета через {} сек.".format(sleep_time)
            )
            time.sleep(sleep_time)
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
        """
        Чтобы получить все части отчета,
        генерирует параметры для новых запросов к апи.

        Формирование дополнительных запросов.
        Они будут сделаны, если отсюда вернется
        непустой массив с набором параметров для запросов.

        :param api_params: dict : входящие параметры класса
        :param current_request_kwargs: dict : {headers, data, url, params} : параметры текущего запроса
        :param request_kwargs_list: list :
            Наборы параметров для запросов, которые будут сделаны.
            В него можно добавлять дополнительные наборы параметров, чтоб сделать дополнительные запросы.
        :param response: request_object : текущий ответ
        :param current_result: json : текущий результат
        :return: list : request_kwargs_list
        """
        # request_kwargs_list может содержать наборы параметров запросов, которые еще не сделаны.
        # Поэтому в него нужно добавлять новые, а не заменять.
        if (
            api_params.get("receive_all_data", False)
            and response.url.find("download") > -1
        ):
            url = current_request_kwargs["url"]
            part = int(re.findall(r"part/([0-9]*)/", url)[0])
            new_part = part + 1
            logging.info(
                "Включен режим получения всех данных. "
                "Запрашиваю следующую часть отчета: {}".format(new_part)
            )
            new_url = re.sub(r"part/[0-9]*/", "part/{}/".format(new_part), url)
            new_request_kwargs = {**current_request_kwargs, "url": new_url}
            request_kwargs_list.append(new_request_kwargs)

        return request_kwargs_list

    def fill_resource_template_url(self, template, params):
        """
        Заполнение параметрами, адреса ресурса из которого формируется URL.

        :param template: str : ресурс
        :param params: dict : параметры
        :return:
        """
        if template.find("/part/") > -1 and not params.get("partNumber"):
            # Принудительно добавляет параметр partNumber, если его нет.
            params.update(partNumber=0)
        return template.format(**params)


class YandexMetrikaStatsClientAdapter(YandexMetrikaManagementClientAdapter):
    resource_mapping = STATS_RESOURCE_MAPPING

    def retry_request(
        self, response, tapi_exception, api_params, count_request_error, *args, **kwargs
    ):
        """
        Условия повторения запроса.
        Если вернет True, то запрос повторится.

        response = tapi_exception.client().response
        status_code = tapi_exception.client().status_code
        response_data = tapi_exception.client().data
        """
        status_code = tapi_exception.client().status_code
        response_data = tapi_exception.client().data or {}
        error_code = int(response_data.get("code", 0))
        errors_types = [i.get("error_type") for i in response_data.get("errors", [])]

        limit_errors = {
            "quota_requests_by_uid": "Превышен лимит количества запросов к API в сутки для пользователя.",
            "quota_delegate_requests": "Превышен лимит количества запросов к API на добавление представителей в час для пользователя.",
            "quota_grants_requests": "Превышен лимит количества запросов к API на добавление доступов к счетчику в час",
            "quota_requests_by_ip": "Превышен лимит количества запросов к API в секунду для IP адреса.",
            "quota_parallel_requests": "Превышен лимит количества параллельных запросов к API в сутки для пользователя.",
            "quota_requests_by_counter_id": "Превышен лимит количества запросов к API в сутки для счётчика.",
        }

        if error_code == 429:
            if "quota_requests_by_ip" in errors_types:
                retry_seconds = random.randint(1, 30)
                error_text = "{}\nПовторный запрос через {} сек.".format(
                    limit_errors["quota_requests_by_ip"], retry_seconds
                )
                logging.warning(error_text)
                time.sleep(retry_seconds)
                return True
            else:
                for err in errors_types:
                    logging.error(limit_errors[err])

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
        """
        Чтобы получить все строки отчета,
        генерирует параметры для новых запросов к апи.

        Формирование дополнительных запросов.
        Они будут сделаны, если отсюда вернется
        непустой массив с набором параметров для запросов.

        :param api_params: dict : входящие параметры класса
        :param current_request_kwargs: dict : {headers, data, url, params} : параметры текущего запроса
        :param request_kwargs_list: list :
            Наборы параметров для запросов, которые будут сделаны.
            В него можно добавлять дополнительные наборы параметров, чтоб сделать дополнительные запросы.
        :param response: request_object : текущий ответ
        :param current_result: json : текущий результат
        :return: list : request_kwargs_list
        """
        # request_kwargs_list может содержать наборы параметров запросов, которые еще не сделаны.
        # Поэтому в него нужно добавлять новые, а не заменять.
        total_rows = int(current_result["total_rows"])
        sampled = current_result["sampled"]

        logging.info("Наличие семплирования: " + str(sampled))
        limit = current_request_kwargs["params"].get("limit", 10000)
        offset = current_result["query"]["offset"] + limit

        if offset <= total_rows:
            logging.info(
                "Получено строк {}. Всего строк {}".format(offset - 1, total_rows)
            )
            if api_params.get("receive_all_data", False):
                logging.info(
                    "Включен режим получения всех данных. "
                    "Запрашиваю следующие части отчета."
                )
                new_request_kwargs = current_request_kwargs.copy()
                new_request_kwargs["params"]["offset"] = offset
                request_kwargs_list.append(new_request_kwargs)
        return request_kwargs_list

    def transform(self, data, request_kwargs, response, api_params, *args, **kwargs):
        """Преобразование данных."""
        new_data = []
        columns = data[0]["query"]["dimensions"] + data[0]["query"]["metrics"]
        for result in data:
            data = result.pop("data")
            for row in data:
                dimensions = [i["name"] for i in row["dimensions"]]
                metrics = row["metrics"]
                new_data.append(dimensions + metrics)
        return [columns] + new_data

    def transform_results(self, results, requests_kwargs, responses, api_params):
        """
        Преобразователь данных после получения всех ответов.

        :param results: list : данные всех запросов
        :param requests_kwargs: list : параметры всех запросов
        :param responses: list : ответы всех запросов
        :param api_params: dict : входящие параметры класса
        :return: list
        """
        return results


YandexMetrikaStats = generate_wrapper_from_adapter(YandexMetrikaStatsClientAdapter)
YandexMetrikaLogsapi = generate_wrapper_from_adapter(YandexMetrikaLogsapiClientAdapter)
YandexMetrikaManagement = generate_wrapper_from_adapter(
    YandexMetrikaManagementClientAdapter
)
