#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re

with open("README.md", "r", encoding="utf8") as fh:
    readme = fh.read()

package = "tapi_yandex_metrika"


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(
        1
    )


setup(
    name="tapi-yandex-metrika",
    version=get_version(package),
    description="Python библиотека для API Яндекс Метрики",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Pavel Maksimov",
    author_email="vur21@ya.ru",
    url="https://github.com/pavelmaksimov/tapi-yandex-metrika",
    packages=[package],
    include_package_data=True,
    install_requires=["requests-oauthlib>=0.4.2", "simplejson", "tapi-wrapper==2019.12.10"],
    license="MIT",
    zip_safe=False,
    keywords="tapi,wrapper,yandex,metrika,api",
    test_suite="tests",
)
