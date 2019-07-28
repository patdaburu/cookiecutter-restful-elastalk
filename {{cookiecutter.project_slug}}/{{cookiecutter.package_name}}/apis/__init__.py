#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: {{cookiecutter.package_name}}.apis.languages
.. moduleauthor:: {{cookiecutter.author_name}} <{{cookiecutter.author_email}}>

This module defines the API and all the namespaces.
"""
from flask_restplus import Api
from .. import __version__
from .info import api as info
from .languages import api as languages

API_ROOT: str = '{{cookiecutter.api_root}}'  #: the common root for API routes

# Create the API object.
api = Api(
    title='{{cookiecutter.project_slug}}',
    version=__version__,
    description='{{cookiecutter.project_description}}'
    # Add other API metadata here.
)

# Add the namespaces.
api.add_namespace(info, path=f'/info')
api.add_namespace(languages, path=f'/languages')
