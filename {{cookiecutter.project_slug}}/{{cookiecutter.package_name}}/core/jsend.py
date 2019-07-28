#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: {{cookiecutter.package_name}}.core.jsend
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

This module contains helper functions that help you model your API responses
consistently using the `JSend <https://labs.omniti.com/labs/jsend>`_
specification.
"""
from enum import Enum
from typing import Dict


class JSendStatus(Enum):
    """
    :cvar SUCCESS: All went well and (usually) some data is returned.
    :cvar FAIL: There was a problem with the data submitted or some
        pre-condition of the API wasn't satisfied.
    :cvar ERROR: An error occurred in processing the request.
    """
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'

    @staticmethod
    def http_code(status: 'JSendStatus') -> int:
        """
        Get the default `HTTP code <https://restfulapi.net/http-status-codes/>`_
        that corresponds to a `JSendStatus`.

        :param status: the status
        :return: the HTTP code
        """
        return {
            JSendStatus.SUCCESS: 200,
            JSendStatus.FAIL: 400,
            JSendStatus.ERROR: 500
        }.get(status)


def response(
        status: JSendStatus,
        message: str = None,
        data: Dict = None,
        code: int = None):
    """
    Construct a `JSend <https://labs.omniti.com/labs/jsend>`_ response message.

    :param status: the general status
    :param message: the message
    :param data: the response data
    :param code: the HTTP code
    :return: the response message
    """
    _code = code if code else JSendStatus.http_code(status)
    return {
        k: v for k, v in {
            'status': status.value,
            'message': message,
            'data': data,
            'code': code if code else JSendStatus.http_code(status)
        }.items() if v
    }, _code
