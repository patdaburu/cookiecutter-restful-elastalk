#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: {{cookiecutter.package_name}}.core.ids
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

You need to identify things and this module can help.
"""
from flask_restplus import fields


class UUID(fields.Raw):
    """
    This is a custom `Flask-RESTplus <https://bit.ly/2ycjt83>`_ that models
    a unique identifier (UUID).
    """
    def format(self, value):
        return str(value)
