# -*- coding: utf-8 -*-
import logging


class YandexMetrikaApiError(Exception):
    def __init__(self, response, message=None, *args, **kwargs):
        self.response = response
        self.message = message

    def __str__(self):
        logging.info("HEADERS = " + str(self.response.headers))
        logging.info("URL = " + self.response.url)
        return "{} {} {} {}".format(
            self.response.status_code,
            self.response.reason,
            self.message or "",
            self.response.text
        )


class YandexMetrikaServerError(YandexMetrikaApiError):
    pass


class YandexMetrikaClientError(YandexMetrikaApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jdata = self.response.json()
        self.code = self.jdata.get("code")
        self.message = self.jdata.get("message")
        self.errors = self.jdata.get("errors")

    def __str__(self):
        logging.info("HEADERS = " + str(self.response.headers))
        logging.info("URL = " + self.response.url)
        return "code={}, message={}, errors={}".format(
            self.code, self.message, self.errors
        )


class YandexMetrikaTokenError(YandexMetrikaClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class YandexMetrikaLimitError(YandexMetrikaApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return (
            "{} {} Исчерпан лимит запросов. "
            "Повторите запрос через некоторое время.\n "
            "{}".format(
                self.response.status_code, self.response.reason, self.response.text
            )
        )
