#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: {{cookiecutter.package_name}}.config
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

This is the general configuration module.
"""
from pathlib import Path
import os

basedir = str(Path(__file__).resolve().parent)  #: the project's base directory


class Config(object):
    """
    This is the base class for configuration objects.
    """
    DEBUG = True if os.environ.get('DEBUG') == 'True' else False
    TESTING = True if os.environ.get('TESTING') == 'True' else False
    CSRF_ENABLED = False if os.environ.get('CSRF_ENABLED') == 'False' else True
    ES_HOSTS = os.environ.get('ES_HOSTS') or ['127.0.0.1']


class ProductionConfig(Config):
    """
    This is the production configuration.
    """
    DEBUG = False


class StagingConfig(Config):
    """
    This is the staging configuration.
    """
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
    This is the development configuration.
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    This is the testing configuration.
    """
    TESTING = True


def get_name() -> str:
    """
    Get the simple name of the current configuration environment.

    :return: the simple name (*e.g.* 'production', or 'development', *etc.*)
    """
    return os.environ.get('FLASK_ENV', 'production')


def get_object_name() -> str:
    """
    Get the name of the configuration object.

    :return: the fully-qualified name of the configuration object
    """
    return f"{__name__}.{get_name().title()}Config"
